#pragma once

#include <cmath>
#include <fftw3.h>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>

std::random_device rd;
std::mt19937_64 rand_gen(rd());
std::uniform_real_distribution<double> unif(-1, 1);
std::normal_distribution<double> normal(0);

// Write an fftw_complex array to the given binary file.
void write_array(const std::string& name, fftw_complex* a, const int& n, const int& d) {
    std::ofstream file(name, std::ios::out | std::ios::binary);
    file.write((char*) &n, sizeof(n));
    file.write((char*) &d, sizeof(d));
    file.write((char*) a, 2 * pow(n, d) * sizeof(double));
    file.close();
}

// Fill an array with DFT frequencies assuming a spatial interval of [-L, L].
// This should produce the same output as numpy.fft.fftfreq().
void fill_freq_1d(double* freq, const int& N, const double& L = 1.0) {
    int N_half = N % 2 ? (N + 1) / 2 : N / 2;
    for (int i = 0; i < N_half; i++)
        freq[i] = M_PI * i * (N - 1) / (N * L);
    for (int i = N_half; i < N; i++)
        freq[i] = M_PI * (i - N) * (N - 1) / (N * L);
}

void fill_gaussian_1d(fftw_complex* in, const int& n, const double& L = 10,
                      const double& alpha = 1.0, const double& a = 0) {
    double x;
    for (int i = 0; i < n; i++) {
        x = -L + 2 * L / (n - 1) * i;
        in[i][0] = exp(-alpha * (x - a) * (x - a));
        in[i][1] = 0;
    }
}

void fill_gaussian_2d(fftw_complex* in, const int& n, const double& L = 10,
                      const double& h=1.0) {
    double x, y;
    double norm = std::pow(2*M_PI*h*h, -1);
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            x = -L + 2 * L / (n - 1) * j;
            y = -L + 2 * L / (n - 1) * i;
            in[i * n + j][0] = norm*exp(-(x*x+y*y)/(2*h*h));
            in[i][1] = 0;
        }
    }
}

void fill_gaussian_3d(fftw_complex* in, const int& n, const double& L = 10,
                      const double& h=1.0) {
    double x, y, z;
    double norm = std::pow(4*M_PI*h*h, -3/2);
    for (size_t i = 0; i < n; i++) {
        for (size_t j = 0; j < n; j++) {
            for (size_t k = 0; j < n; j++) {
                x = -L + 2 * L / (n - 1) * j;
                y = -L + 2 * L / (n - 1) * i;
                z = -L + 2 * L / (n - 1) * i;
                int p = n * n * i + n * j + k;
                in[p][0] = norm*exp(-(x*x+y*y+z*z)/(4*h*h));
                in[i][1] = 0;
            }
        }
    }
}

// Fills an fftw_complex array a (side = n, dimension = d) with real
// random numbers drawn from a normal distribution with variance "sigma"
// and mean "mu".
void fill_random(fftw_complex* a, const int& n, const int& d = 1, const double& mu = 0,
                 const double& sigma = 1.0) {
    int N = std::pow(n, d);
    double mean = 0;
    for (int i = 0; i < N; i++) {
        a[i][0] = sigma * normal(rd);
        a[i][1] = 0;
        mean += a[i][0];
    }

    // Make sure that the array mean is exact.
    mean /= N;
    for (int i = 0; i < N; i++)
        a[i][0] += mu - mean;
}

void fftshift_1d(fftw_complex* a, const int& n) {
    int n_half = n / 2;
    for (int i = 0; i < n_half; i++) {
        std::swap(a[i][0], a[n_half + i][0]);
        std::swap(a[i][1], a[n_half + i][1]);
    }
}

void fftshift_2d(fftw_complex* a, const int& n) {
    int n_half = n / 2;

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n_half; j++) {
            int p = n * i + j;
            int q = n * i + n_half + j;
            std::swap(a[p][0], a[q][0]);
            std::swap(a[p][1], a[q][1]);
        }

    for (int i = 0; i < n_half; i++)
        for (int j = 0; j < n; j++) {
            int p = n * i + j;
            int q = n * (i + n_half) + j;
            std::swap(a[p][0], a[q][0]);
            std::swap(a[p][1], a[q][1]);
        }
}

void fftshift_3d(fftw_complex* a, const int& n) {
    int n_half = n / 2;

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n_half; k++) {
                int p = n * n * i + n * j + k;
                int q = n * n * i + n * j + (k + n_half);
                std::swap(a[p][0], a[q][0]);
                std::swap(a[p][1], a[q][1]);
            }

    for (int i = 0; i < n; i++)
        for (int j = 0; j < n_half; j++)
            for (int k = 0; k < n; k++) {
                int p = n * n * i + n * j + k;
                int q = n * n * i + n * (j + n_half) + k;
                std::swap(a[p][0], a[q][0]);
                std::swap(a[p][1], a[q][1]);
            }

    for (int i = 0; i < n_half; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++) {
                int p = n * n * i + n * j + k;
                int q = n * n * (i + n_half) + n * j + k;
                std::swap(a[p][0], a[q][0]);
                std::swap(a[p][1], a[q][1]);
            }
}

// Helper function to print "square" fftw_complex arrays for dimensions 1, 2, and 3.
void print_array(fftw_complex* a, const int& n, const int& d = 1, const std::string& sep = "   ",
                 const int& precision = 3) {
    int nx = n;
    int ny = d >= 2 ? n : 1;
    int nz = d == 3 ? n : 1;

    std::cout << std::scientific << std::setprecision(precision);
    for (int i = 0; i < nz; i++) {
        for (int j = 0; j < ny; j++) {
            for (int k = 0; k < nx; k++) {
                int p = (nx * ny) * i + ny * j + k;
                std::cout << "(" << a[p][0] << ", " << a[p][1] << ")";
                if (k < nx - 1)
                    std::cout << sep;
            }
            if (ny > 1 && (j < ny - 1 || nz > 1))
                std::cout << sep;
            std::cout << std::endl;
        }
        if (nz > 1)
            std::cout << std::endl;
    }
}

void fill_array(fftw_complex* a, const int& n) {
    for (int i = 0; i < n; i++) {
        a[i][0] = i;
        a[i][1] = i;
    }
}

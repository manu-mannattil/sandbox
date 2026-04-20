// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=c++}
// com: : ${CXXFLAGS:=-Wall -Werror -lm -lfftw3 -lfftw3_omp -fopenmp -Ofast}
// com: \{ ${CXX} {} ${CXXFLAGS} -o {.}; \}

#include <chrono>
#include <cstdlib>
#include <fftw3.h>
#include <iostream>
#include <math.h>
#include <omp.h>
#include <random>

using namespace std;

random_device rd;
mt19937_64 rand_gen(rd());
uniform_real_distribution<double> unif(-1, 1);

int main(int argc, const char* argv[]) {
    long N = pow(2, 9);
    int threads = 1;

    fftw_init_threads();
    if (argc == 2)
        threads = atoi(argv[1]);

    fftw_plan_with_nthreads(threads);

    // Complex input/ouput of size NxN.
    // The arrays themselves are 1D arrays, so you'll have to do the indexing yourself.
    fftw_complex* phi = fftw_alloc_complex(N * N * N);
    fftw_complex* phi_q = fftw_alloc_complex(N * N * N);
    fftw_plan p = fftw_plan_dft_3d(N, N, N, phi, phi_q, FFTW_FORWARD, FFTW_MEASURE);

    // Initialize Gaussian input.
    for (long i = 0; i < N * N * N; i++) {
        phi[i][0] = unif(rand_gen);
        phi[i][1] = unif(rand_gen);
    }

    auto start = chrono::high_resolution_clock::now();
    int runs = 5;
    for (int i = 0; i < runs; i++) {
        fftw_execute(p);
    }
    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> duration = end - start;
    cout << "time = " << duration.count() / runs << "s" << endl;

    fftw_destroy_plan(p);
    fftw_free(phi);
    fftw_free(phi_q);
    fftw_cleanup_threads();

    return 0;
}

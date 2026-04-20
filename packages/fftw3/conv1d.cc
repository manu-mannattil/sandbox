// FFT based convolution of two Gaussians in 1D.  The result is also
// a Gaussian, which enables a simple check.
//
// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=c++}
// com: : ${CXXFLAGS:=-Wall -Werror -lm -lfftw3}
// com: \{ ${CXX} {} ${CXXFLAGS} -o ${TMPDIR}/{!}; \} && ${TMPDIR}/{!} {@}

#include <algorithm>
#include <cmath>
#include <fftw3.h>
#include <iostream>
#include <utils.h>

using namespace std;

int main(int argc, const char* argv[]) {
    int N = 1024;
    double L = 10;
    double dx = 2 * L / N;

    // Convolution kernel is an off-centered Gaussian.
    double alpha = 1.0, a = -4.0;
    fftw_complex* K = fftw_alloc_complex(N);
    fill_gaussian_1d(K, N, L, alpha, a);

    // DFTs assume that the "origin" of the kernel at the "ends".
    // But the kernel we've defined above has an origin at the center.
    // So shift appropriately to put the origin at the "ends" beforing
    // taking the Fourier transform.
    fftshift_1d(K, N);
    fftw_complex* K_q = fftw_alloc_complex(N);
    fftw_plan plan_K_q = fftw_plan_dft_1d(N, K, K_q, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(plan_K_q);

    // Function is also an off-centered Gaussian.
    double beta = 0.5, b = 3.0;
    fftw_complex* phi = fftw_alloc_complex(N);
    fill_gaussian_1d(phi, N, L, beta, b);

    fftw_complex* phi_q = fftw_alloc_complex(N);
    fftw_plan plan_phi_q = fftw_plan_dft_1d(N, phi, phi_q, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(plan_phi_q);

    // FT of convolution is product of FTs.
    fftw_complex* K_phi_q = fftw_alloc_complex(N);
    for (int i = 0; i < N; i++) {
        // Mulitipying by dx is to convert the sum into a integral.
        // Dividing by N is to ensure that FFTW's backward transform gives the actual inverse.
        K_phi_q[i][0] = (K_q[i][0] * phi_q[i][0] - K_q[i][1] * phi_q[i][1]) * dx / N;
        K_phi_q[i][1] = (K_q[i][0] * phi_q[i][1] + K_q[i][1] * phi_q[i][0]) * dx / N;
    }

    // Take inverse transform.
    fftw_complex* K_phi = fftw_alloc_complex(N);
    fftw_plan plan_K_phi = fftw_plan_dft_1d(N, K_phi_q, K_phi, FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_execute(plan_K_phi);

    write_array("conv1d.bin", K_phi, N, 1);

    fftw_destroy_plan(plan_K_q);
    fftw_free(K_q);
    fftw_free(K);

    fftw_destroy_plan(plan_phi_q);
    fftw_free(phi_q);
    fftw_free(phi);

    fftw_destroy_plan(plan_K_phi);
    fftw_free(K_phi_q);
    fftw_free(K_phi);

    return 0;
}

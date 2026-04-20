// Compute the DFT of a 1D Gaussian and verify that the result is correct.
//
// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=c++}
// com: : ${CXXFLAGS:=-Wall -Werror -lm -lfftw3}
// com: \{ ${CXX} {} ${CXXFLAGS} -o ${TMPDIR}/{!}; \} && ${TMPDIR}/{!} {@}

#include <fftw3.h>
#include <iostream>
#include <math.h>
#include <utils.h>

using namespace std;

int main(int argc, const char* argv[]) {
    int N = 1024;
    double L = 10;

    // Input is a 1D Gaussian.
    fftw_complex* phi = fftw_alloc_complex(N);
    fill_gaussian_1d(phi, N, L);

    // Fourier transform will be stored here.
    fftw_complex* phi_q = fftw_alloc_complex(N);

    // Set up Fourier frequencies.
    double q[N];
    fill_freq_1d(q, N, L);

    fftw_plan p = fftw_plan_dft_1d(N, phi, phi_q, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(p);

    // Compute derivative in Fourier space.
    fftw_complex* dphi_q = fftw_alloc_complex(N);
    for (int i = 0; i < N; i++) {
        dphi_q[i][0] = -phi_q[i][1] * q[i] / N;
        dphi_q[i][1] = phi_q[i][0] * q[i] / N;
    }

    // Backward transform to find derivative in real space.
    fftw_complex* dphi = fftw_alloc_complex(N);
    fftw_plan p_deriv = fftw_plan_dft_1d(N, dphi_q, dphi, FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_execute(p_deriv);

    write_array("1dgauss-deriv.bin", dphi, N, 1);

    fftw_destroy_plan(p);
    fftw_destroy_plan(p_deriv);
    fftw_free(phi);
    fftw_free(phi_q);
    fftw_free(dphi);
    fftw_free(dphi_q);

    return 0;
}

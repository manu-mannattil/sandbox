// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=c++}
// com: : ${CXXFLAGS:=-Wall -Werror -lm -lfftw3}
// com: \{ ${CXX} {} ${CXXFLAGS} -o ${TMPDIR}/{!}; \} && ${TMPDIR}/{!} {@}

#include <fftw3.h>
#include <iostream>
#include <utils.h>

using namespace std;

int main(int argc, const char* argv[]) {
    int N = 1024;
    double L = 10;

    // Complex input/ouput of size NxN.
    // The arrays themselves are 1D arrays, so you'll have to do the indexing yourself.
    fftw_complex* phi = fftw_alloc_complex(N * N);
    fftw_complex* phi_q = fftw_alloc_complex(N * N);

    // Initialize Gaussian input.
    fill_gaussian_2d(phi, N);

    fftw_plan p = fftw_plan_dft_2d(N, N, phi, phi_q, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(p);

    // Set up Fourier frequencies.
    double q[N];
    fill_freq_1d(q, N, L);

    // x derivative --------------------------------------------------------

    fftw_complex* dxphi_q = fftw_alloc_complex(N * N);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            dxphi_q[i * N + j][0] = -q[j] * phi_q[i * N + j][1] / N;
            dxphi_q[i * N + j][1] = q[j] * phi_q[i * N + j][0] / N;
        }
    }

    fftw_complex* dxphi = fftw_alloc_complex(N * N);

    fftw_plan plan_dxphi = fftw_plan_dft_2d(N, N, dxphi_q, dxphi, FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_execute(plan_dxphi);
    write_array("2dgauss-dx.bin", dxphi, N, 2);
    fftw_free(dxphi);
    fftw_free(dxphi_q);
    fftw_destroy_plan(plan_dxphi);

    // Laplacian -----------------------------------------------------------

    fftw_complex* d2phi_q = fftw_alloc_complex(N * N);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            d2phi_q[i * N + j][0] = -(q[j] * q[j] + q[i] * q[i]) * phi_q[i * N + j][0] / N;
            d2phi_q[i * N + j][1] = -(q[j] * q[j] + q[i] * q[i]) * phi_q[i * N + j][1] / N;
        }
    }

    fftw_complex* d2phi = fftw_alloc_complex(N * N);

    fftw_plan plan_d2phi = fftw_plan_dft_2d(N, N, d2phi_q, d2phi, FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_execute(plan_d2phi);
    write_array("2dgauss-d2.bin", d2phi, N, 2);
    fftw_free(d2phi);
    fftw_free(d2phi_q);
    fftw_destroy_plan(plan_d2phi);

    fftw_destroy_plan(p);
    fftw_free(phi);
    fftw_free(phi_q);

    return 0;
}

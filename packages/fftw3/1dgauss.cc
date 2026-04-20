// Compute the DFT of a 1D Gaussian and verify that the result is correct.
//
// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=clang++}
// com: : ${CXXFLAGS:=-Wall -Werror -I"${MKLROOT}/include/fftw" -lm -lfftw3}
// com: \{ ${CXX} {} ${CXXFLAGS} -o ${TMPDIR}/{!}; \} && ${TMPDIR}/{!} {@}

#include <fftw3.h>
#include <iostream>
#include <math.h>
#include <utils.h>

using namespace std;

int main(int argc, const char* argv[]) {
    // Length of the DFT.
    size_t N = 1024;

    // Complex input of size N is in "phi_q".
    // phi_q is initialized with a Gaussian.
    fftw_complex* phi = fftw_alloc_complex(N);
    fill_gaussian_1d(phi, N);

    // Complex output of size N is stored in "phi_q".
    fftw_complex* phi_q = fftw_alloc_complex(N);

    // Now that we've allocated memory, set up a plan and do the DFT.
    fftw_plan p = fftw_plan_dft_1d(N, phi, phi_q, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(p);

    write_array("1dgauss.bin", phi_q, N, 1);

    fftw_destroy_plan(p);
    fftw_free(phi);
    fftw_free(phi_q);

    return 0;
}

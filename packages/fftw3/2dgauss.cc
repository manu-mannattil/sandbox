// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=c++}
// com: : ${CXXFLAGS:=-Wall -Werror -lm -lfftw3}
// com: \{ ${CXX} {} ${CXXFLAGS} -o ${TMPDIR}/{!}; \} && ${TMPDIR}/{!} {@}

#include <fftw3.h>
#include <iostream>
#include <utils.h>

using namespace std;

int main(int argc, const char* argv[]) {
    size_t N = 1024;

    // Complex input/ouput of size NxN.
    // The arrays themselves are 1D arrays, so you'll have to do the indexing yourself.
    fftw_complex* phi = fftw_alloc_complex(N * N);
    fftw_complex* phi_q = fftw_alloc_complex(N * N);

    // Initialize Gaussian input.
    fill_gaussian_2d(phi, N);

    fftw_plan p = fftw_plan_dft_2d(N, N, phi, phi_q, FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(p);

    write_array("2dgauss.bin", phi_q, N, 2);

    fftw_destroy_plan(p);
    fftw_free(phi);
    fftw_free(phi_q);

    return 0;
}

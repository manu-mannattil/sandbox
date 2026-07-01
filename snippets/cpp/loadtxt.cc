// com: : ${TMPDIR:=/tmp}
// com: : ${CXX:=c++}
// com: : ${CXXFLAGS:=-Wall -Werror -Wfatal-errors}
// com: \{ ${CXX} {} ${CXXFLAGS} -o ${TMPDIR}/{!}; \} && ${TMPDIR}/{!} {@}
//
// A function that's analogous to NumPy's loadtxt.
// This will handle non-rectangular data, i.e., those with different
// numbers of columns in each row.
//

#include <fstream>
#include <regex>
#include <stdexcept>
#include <string>
#include <vector>

std::vector<std::vector<double>> loadtxt(const std::string& filename) {
    std::ifstream fin(filename);
    if (!fin)
        throw std::runtime_error("Could not open file.");

    std::vector<std::vector<double>> data;
    std::string line;

    // Regular expression for delimiter patterns.
    std::regex delim_re("\\s+");

    while (std::getline(fin, line)) {
        // Skip blank lines.
        if (line.find_first_not_of(" \t\r\n") == std::string::npos)
            continue;

        // Skip comments.
        if (line[line.find_first_not_of(" \t")] == '#')
            continue;

        std::vector<double> row;

        std::sregex_token_iterator it(line.begin(), line.end(), delim_re, -1);
        std::sregex_token_iterator end;

        for (; it != end; ++it) {
            if (it->str().empty())
                continue;

            row.push_back(std::stod(it->str()));
        }

        data.push_back(std::move(row));
    }

    return data;
}

// Test ----------------------------------------------------------------

#include <iostream>

int main(int argc, const char* argv[]) {
    std::string name = "loadtxt.dat";

    auto data = loadtxt(name);

    for (const auto& row : data) {
        for (const auto& col : row) {
            std::cout << col << "\t";
        }
        std::cout << std::endl;
    }

    return 0;
}

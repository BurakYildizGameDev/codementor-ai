// EXPECT: 5, 7
#include <cstddef>

void fill(std::size_t n) {
    int* data = new int[n];
    for (std::size_t i = 0; i < n; ++i) data[i] = 0;
    delete[] data;
}

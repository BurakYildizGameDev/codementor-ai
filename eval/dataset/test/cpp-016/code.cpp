#include <iostream>
#include <vector>

void print_reversed(const std::vector<int>& v) {
    for (std::size_t i = v.size() - 1; i >= 0; --i) {
        std::cout << v[i] << '\n';
    }
}

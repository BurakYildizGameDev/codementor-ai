#include <vector>

void fill(std::vector<int>& v, int n) {
    v.reserve(n);
    for (int i = 0; i < n; ++i) {
        v.push_back(i);
    }
}

void grow(std::vector<int>& v, const std::vector<int>& src) {
    v.resize(src.size());
    for (int x : src) {
        v.push_back(x);
    }
}

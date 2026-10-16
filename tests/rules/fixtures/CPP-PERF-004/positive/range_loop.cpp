// EXPECT: 6, 12
#include <vector>

void copy_all(std::vector<int>& out, const std::vector<int>& src) {
    for (int x : src) {
        out.push_back(x);
    }
}

void squares(std::vector<int>& out, int n) {
    for (int i = 0; i < n; ++i) {
        out.emplace_back(i * i);
    }
}

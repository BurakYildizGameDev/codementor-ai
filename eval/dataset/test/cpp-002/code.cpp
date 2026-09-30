#include <vector>

int sum(const std::vector<int& values) {
    int total = 0;
    for (int v : values) {
        total += v;
    }
    return total;
}

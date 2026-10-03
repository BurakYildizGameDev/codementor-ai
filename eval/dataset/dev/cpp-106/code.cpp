#include <vector>

int sum_elements(const std::vector<int>& vec) {
    int total = 0;
    for (size_t i = 0; i <= vec.size(); ++i) {
        total += vec[i];
    }
    return total;
}

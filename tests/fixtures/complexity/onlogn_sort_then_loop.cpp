// expect-hint: n log n | high
#include <algorithm>
#include <vector>

int count_unique(std::vector<int> values) {
    std::sort(values.begin(), values.end());
    int unique = 0;
    for (size_t i = 0; i < values.size(); ++i) {
        if (i == 0 || values[i] != values[i - 1]) {
            ++unique;
        }
    }
    return unique;
}

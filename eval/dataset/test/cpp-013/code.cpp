#include <algorithm>
#include <vector>

std::vector<int> first_occurrences(const std::vector<int>& input) {
    std::vector<int> result;
    for (int x : input) {
        if (std::find(result.begin(), result.end(), x) == result.end()) {
            result.push_back(x);
        }
    }
    return result;
}

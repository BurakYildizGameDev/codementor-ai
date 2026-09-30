#include <algorithm>
#include <vector>

void sort_desc(std::vector<int>& v) {
    std::sort(v.begin(), v.end(), [](int a, int b) {
        return a > b;
    };
}

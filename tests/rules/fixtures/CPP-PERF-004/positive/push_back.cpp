// EXPECT: 6
#include <vector>

void fill(std::vector<int>& v, int n) {
    for (int i = 0; i < n; ++i) {
        v.push_back(i);
    }
}

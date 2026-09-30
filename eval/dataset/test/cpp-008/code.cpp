#include <vector>

void duplicate_evens(std::vector<int>& v) {
    for (int x : v) {
        if (x % 2 == 0) {
            v.push_back(x);
        }
    }
}

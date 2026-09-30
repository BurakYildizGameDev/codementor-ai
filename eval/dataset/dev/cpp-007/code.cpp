#include <vector>

void remove_negatives(std::vector<int>& v) {
    for (std::size_t i = 0; i < v.size();) {
        if (v[i] < 0) {
            v.erase(v.begin() + i);
        } else {
            ++i;
        }
    }
}

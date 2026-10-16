#include <vector>

void drain(std::vector<int>& v, int n) {
    int i = 0;
    while (i < n) {
        v.push_back(i++);
    }
}

void maybe(std::vector<int>& v, int n) {
    for (int i = 0; i < n; ++i) {
        if (i % 2 == 0) {
            v.push_back(i);
        }
    }
}

void early(std::vector<int>& v, int n) {
    for (int i = 0; i < n; ++i) {
        if (i > 100) {
            break;
        }
        v.push_back(i);
    }
}

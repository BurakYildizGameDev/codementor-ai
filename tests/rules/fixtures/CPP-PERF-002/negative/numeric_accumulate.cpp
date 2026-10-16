#include <string>

int sum(int n) {
    int total = 0;
    for (int i = 0; i < n; ++i) {
        total = total + i;
    }
    return total;
}

std::string label(int n) {
    std::string out;
    for (int i = 0; i < n; ++i) {
        out = "item" + std::to_string(i);
    }
    return out;
}

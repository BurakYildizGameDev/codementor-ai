// EXPECT: 5, 11
#include <string>
#include <vector>

int total(std::vector<int> values) {
    int s = 0;
    for (int v : values) s += v;
    return s;
}

bool has_prefix(const std::string text, const std::string& prefix) {
    return text.rfind(prefix, 0) == 0;
}

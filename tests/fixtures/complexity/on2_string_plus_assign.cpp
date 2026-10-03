// expect-hint: n^2 | high
#include <string>
#include <vector>

std::string join(const std::vector<std::string>& words) {
    std::string result;
    for (const auto& w : words) {
        result = result + w;
    }
    return result;
}

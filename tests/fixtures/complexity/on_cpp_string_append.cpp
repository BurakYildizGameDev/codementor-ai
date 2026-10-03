// expect-hint: n | high
#include <string>
#include <vector>

std::string join(const std::vector<std::string>& words) {
    std::string result;
    for (const auto& w : words) {
        result += w;
    }
    return result;
}

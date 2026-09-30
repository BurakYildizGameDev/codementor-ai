#include <string>
#include <vector>

std::string join(const std::vector<std::string>& parts, const std::string& sep) {
    std::string result;
    for (std::size_t i = 0; i < parts.size(); i++) {
        result = result + parts[i];
        if (i + 1 < parts.size()) {
            result = result + sep;
        }
    }
    return result;
}

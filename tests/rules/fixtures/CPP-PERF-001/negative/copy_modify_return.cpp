#include <algorithm>
#include <cctype>
#include <string>
#include <vector>

std::vector<int> sorted(std::vector<int> v) {
    std::sort(v.begin(), v.end());
    return v;
}

std::string upper(std::string s) {
    for (char& c : s) c = static_cast<char>(std::toupper(c));
    return s;
}

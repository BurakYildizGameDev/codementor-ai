// EXPECT: 7, 15
#include <string>

std::string join(const std::string& other, int n) {
    std::string s;
    for (int i = 0; i < n; ++i) {
        s = s + other + "!";
    }
    return s;
}

std::wstring widen(int n) {
    std::wstring w;
    for (int i = 0; i < n; ++i) {
        w = w + L"?";
    }
    return w;
}

#include <string>

std::string build(int n) {
    std::string s;
    for (int i = 0; i < n; ++i) {
        s += "x";
        s.append("y");
    }
    return s;
}

std::string once(void) {
    std::string s;
    s = s + "yalnızca bir kez";
    return s;
}

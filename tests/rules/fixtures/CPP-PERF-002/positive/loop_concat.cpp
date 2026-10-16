// EXPECT: 7
#include <string>

std::string build(int n) {
    std::string s;
    for (int i = 0; i < n; ++i) {
        s = s + "x";
    }
    return s;
}

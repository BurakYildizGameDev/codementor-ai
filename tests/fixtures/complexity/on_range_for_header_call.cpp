// expect-hint: n | high
#include <string>

int count_upper(const std::string& s) {
    int count = 0;
    for (char c : s.substr(1)) {
        if (c >= 'A' && c <= 'Z') {
            count++;
        }
    }
    return count;
}

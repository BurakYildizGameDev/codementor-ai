#include <string.h>

int count_a(const char *s) {
    int count = 0;
    size_t n = strlen(s);
    for (size_t i = 0; i < n; i++) {
        if (s[i] == 'a') count++;
    }
    for (size_t i = 0, m = strlen(s); i < m; i++) {
        if (s[i] == 'b') count++;
    }
    return count;
}

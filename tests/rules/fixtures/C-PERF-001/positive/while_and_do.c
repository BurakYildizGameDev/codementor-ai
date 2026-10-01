// EXPECT: 6, 16
#include <string.h>

void to_lower(char *s) {
    size_t i = 0;
    while (i < strlen(s)) {
        if (s[i] >= 'A' && s[i] <= 'Z') s[i] += 32;
        i++;
    }
}

size_t skip_spaces(const char *t) {
    size_t j = 0;
    do {
        j++;
    } while (j < strlen(t) && t[j] == ' ');
    return j;
}

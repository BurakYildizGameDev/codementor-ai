// EXPECT: 6
#include <string.h>

int count_upper(const char *s) {
    int count = 0;
    for (size_t i = 0; i < strlen(s); i++) {
        if (s[i] >= 'A' && s[i] <= 'Z') count++;
    }
    return count;
}

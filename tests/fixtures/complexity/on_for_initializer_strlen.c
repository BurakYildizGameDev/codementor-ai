// expect-hint: n | high
#include <string.h>
#include <ctype.h>

void to_upper(char *s) {
    for (size_t i = 0, n = strlen(s); i < n; i++) {
        s[i] = (char)toupper((unsigned char)s[i]);
    }
}

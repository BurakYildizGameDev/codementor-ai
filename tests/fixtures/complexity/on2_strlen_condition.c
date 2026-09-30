// expect-hint: n^2 | high
#include <string.h>
#include <ctype.h>

void to_upper(char *s) {
    for (size_t i = 0; i < strlen(s); i++) {
        s[i] = (char)toupper((unsigned char)s[i]);
    }
}

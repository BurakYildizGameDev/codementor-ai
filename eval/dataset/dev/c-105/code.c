#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *duplicate_uppercase(const char *str) {
    size_t n = strlen(str);
    char *copy = (char *)malloc(n + 1);
    for (size_t i = 0; i < strlen(str); i++) {
        if (str[i] >= 'a' && str[i] <= 'z') {
            copy[i] = str[i] - 32;
        } else {
            copy[i] = str[i];
        }
    }
    copy[n] = '\0';
    return copy;
}

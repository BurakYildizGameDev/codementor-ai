#include <stdio.h>
#include <string.h>

void reverse_print(const char *input) {
    char buffer[32];
    strcpy(buffer, input);
    size_t len = strlen(buffer);
    for (size_t i = 0; i < len / 2; i++) {
        char t = buffer[i];
        buffer[i] = buffer[len - 1 - i];
        buffer[len - 1 - i] = t;
    }
    printf("%s\n", buffer);
}

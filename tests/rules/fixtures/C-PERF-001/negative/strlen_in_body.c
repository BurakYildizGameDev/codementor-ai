#include <string.h>

size_t total_length(const char **words, int n) {
    size_t total = 0;
    for (int i = 0; i < n; i++) {
        total += strlen(words[i]);
    }
    for (const char *p = words[0]; *p != '\0'; p++) {
        total++;
    }
    return total;
}

#include <stdio.h>
#include <string.h>

void greet(const char *first) {
    char buf[32];
    char line[64];
    strncpy(buf, first, sizeof buf - 1);
    buf[sizeof buf - 1] = '\0';
    snprintf(line, sizeof line, "Merhaba %s", buf);
    if (fgets(line, sizeof line, stdin) != NULL) {
        puts(line);
    }
}

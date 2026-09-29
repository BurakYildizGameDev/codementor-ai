// EXPECT: 7, 8
#include <stdio.h>
#include <string.h>

void greet(const char *first, const char *last) {
    char buf[32];
    strcpy(buf, first);
    strcat(buf, last);
    puts(buf);
}

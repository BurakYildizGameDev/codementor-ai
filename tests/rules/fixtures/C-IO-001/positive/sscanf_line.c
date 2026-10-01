// EXPECT: 7
#include <stdio.h>

int parse_age(const char *line) {
    int age = 0;
    if (line[0] != '\0') {
        sscanf(line, "%d", &age);
    }
    return age;
}

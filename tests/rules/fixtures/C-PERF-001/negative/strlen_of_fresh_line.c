#include <stdio.h>
#include <string.h>

int count_lines(FILE *f) {
    char line[256];
    int n = 0;
    while (fgets(line, sizeof line, f) != NULL && strlen(line) > 1) {
        n++;
    }
    return n;
}

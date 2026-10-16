// EXPECT: 7, 8
#include <stdio.h>

int load(FILE *f) {
    char name[16];
    char path[128];
    fscanf(f, "%s", name);
    fscanf(f, "%ls", path);
    return 0;
}

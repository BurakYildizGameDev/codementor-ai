// EXPECT: 5
#include <stdio.h>

void label(char *out, int id) {
    sprintf(out, "item-%d", id);
}

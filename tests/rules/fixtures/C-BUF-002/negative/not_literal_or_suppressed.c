#include <stdio.h>

int parse(const char *fmt) {
    char buf[8];
    scanf("%*s");
    scanf(fmt, buf);
    sscanf("12 34", "%s", buf);
    printf("%s\n", buf);
    return 0;
}

#include <stdio.h>

/* strcpy ve gets burada yalnızca yorumda geçiyor */
static void copy_name(char *dst, const char *src, int n) {
    int i = 0;
    for (; i < n - 1 && src[i] != '\0'; i++) dst[i] = src[i];
    dst[i] = '\0';
}

int main(void) {
    char out[8];
    copy_name(out, "sprintf", 8);
    puts("gets kullanmayin");
    return 0;
}

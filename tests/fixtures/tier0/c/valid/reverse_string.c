#include <stdio.h>
#include <string.h>

/* Metni yerinde ters çevirir; ç, ğ, ş gibi karakterler yorumda sorun çıkarmamalı. */
void reverse(char *s) {
    if (s == NULL) {
        return;
    }
    size_t len = strlen(s);
    for (size_t i = 0, j = len ? len - 1 : 0; i < j; ++i, --j) {
        char tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}

int main(void) {
    char text[] = "merhaba dünya";
    reverse(text);
    puts(text);
    return 0;
}

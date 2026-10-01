#include <stdio.h>

void drain(void) {
    int c;
    /* fflush(stdin) tanımsız davranış; bunun yerine satır sonuna kadar oku */
    while ((c = getchar()) != '\n' && c != EOF) {
    }
    puts("fflush(stdin) kullanma");
}

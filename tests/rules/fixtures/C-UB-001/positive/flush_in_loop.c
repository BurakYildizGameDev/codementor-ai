// EXPECT: 9
#include <stdio.h>

char ask(void) {
    char answer = 0;
    while (answer != 'e' && answer != 'h') {
        printf("Devam? (e/h) ");
        answer = getchar();
        fflush( stdin );
    }
    return answer;
}

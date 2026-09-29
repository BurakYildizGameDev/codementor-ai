#include <stdio.h>

typedef enum { WAIT_FIRST, WAIT_OP, WAIT_SECOND, DONE } State;

static int read_number(double *out) {
    if (scanf("%lf", out) != 1) {
        int c;
        while ((c = getchar()) != '\n' && c != EOF) {
        }
        return 0;
    }
    return 1;
}

int main(void) {
    State state = WAIT_FIRST;
    double a = 0.0, b = 0.0;
    char op = '+';

    while (state != DONE) {
        switch (state) {
        case WAIT_FIRST:
            printf("Birinci sayı: ");
            state = read_number(&a) ? WAIT_OP : WAIT_FIRST;
            break;
        case WAIT_OP:
            printf("İşlem (+ - * /): ");
            if (scanf(" %c", &op) == 1) {
                state = WAIT_SECOND;
            }
            break;
        case WAIT_SECOND:
            printf("İkinci sayı: ");
            if (!read_number(&b)) {
                break;
            }
            if (op == '/' && b == 0.0) {
                puts("Sıfıra bölme tanımsız.");
            } else {
                double r = op == '+' ? a + b : op == '-' ? a - b : op == '*' ? a * b : a / b;
                printf("Sonuç: %g\n", r);
            }
            state = DONE;
            break;
        default:
            state = DONE;
        }
    }
    return 0;
}

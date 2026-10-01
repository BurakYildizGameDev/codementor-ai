#include <stdio.h>

int read_choice(void) {
    int choice;
    if (scanf("%d", &choice) != 1) choice = 0;
    scanf("%*[^\n]");
    scanf("%*c");
    return choice;
}

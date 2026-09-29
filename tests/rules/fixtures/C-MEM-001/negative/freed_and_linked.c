#include <stdlib.h>

struct Node { int value; struct Node *next; };

void push(struct Node **head, int value) {
    struct Node *node = malloc(sizeof *node);
    node->value = value;
    node->next = *head;
    *head = node;
}

int average(const int *src, int n) {
    int *copy = malloc(n * sizeof(int));
    int total = 0;
    for (int i = 0; i < n; i++) { copy[i] = src[i]; total += copy[i]; }
    free(copy);
    return total / n;
}

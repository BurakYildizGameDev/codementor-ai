#include <stdlib.h>

struct Node { int value; struct Node *next; };

struct Node *build(int n) {
    struct Node *head = NULL;
    for (int i = 0; i < n; i++) {
        struct Node *node = malloc(sizeof(struct Node));
        node->value = i;
        node->next = head;
        head = node;
    }
    return head;
}

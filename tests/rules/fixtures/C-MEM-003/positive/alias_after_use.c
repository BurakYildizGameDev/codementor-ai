// EXPECT: 8
#include <stdlib.h>
typedef struct Node { int value; struct Node *next; } Node;

void push_back(Node **head, int value) {
    Node *cur = *head;
    while (cur->next != NULL) cur = cur->next;
    Node *n = malloc(sizeof(Node));
    n->value = value;
    cur->next = n;
}

// EXPECT: 7
#include <stdlib.h>

typedef struct Node { int value; struct Node *next; } Node;

Node *make_node(int v) {
    Node *n = (Node *)malloc(sizeof *n);
    n->value = v;
    n->next = NULL;
    return n;
}

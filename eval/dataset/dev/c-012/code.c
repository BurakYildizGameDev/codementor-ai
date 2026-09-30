#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

void list_free(Node *node) {
    while (node != NULL) {
        free(node);
        node = node->next;
    }
}

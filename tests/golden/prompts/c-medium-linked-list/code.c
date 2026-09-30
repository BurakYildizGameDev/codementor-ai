#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

void push_front(Node **head, int value) {
    Node *n = malloc(sizeof(Node));
    n->value = value;
    n->next = *head;
    *head = n;
}

void push_back(Node **head, int value) {
    Node *n = malloc(sizeof(Node));
    n->value = value;
    n->next = NULL;
    Node *cur = *head;
    while (cur->next != NULL) cur = cur->next;
    cur->next = n;
}

void remove_value(Node **head, int value) {
    Node *cur = *head;
    Node *prev = NULL;
    while (cur != NULL) {
        if (cur->value == value) {
            free(cur);
            if (prev == NULL) *head = cur->next;
            else prev->next = cur->next;
            return;
        }
        prev = cur;
        cur = cur->next;
    }
}

void destroy(Node *head) {
    while (head != NULL) {
        free(head);
        head = head->next;
    }
}

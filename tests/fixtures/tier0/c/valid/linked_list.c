#include <stdio.h>
#include <stdlib.h>

struct node {
    int value;
    struct node *next;
};

static int push_front(struct node **head, int value) {
    struct node *n = malloc(sizeof *n);
    if (n == NULL) {
        return -1;
    }
    n->value = value;
    n->next = *head;
    *head = n;
    return 0;
}

static void remove_value(struct node **head, int value) {
    struct node **cur = head;
    while (*cur != NULL) {
        if ((*cur)->value == value) {
            struct node *victim = *cur;
            *cur = victim->next;
            free(victim);
            return;
        }
        cur = &(*cur)->next;
    }
}

static void destroy(struct node *head) {
    while (head != NULL) {
        struct node *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    struct node *list = NULL;
    for (int i = 0; i < 5; ++i) {
        push_front(&list, i);
    }
    remove_value(&list, 3);
    for (const struct node *n = list; n != NULL; n = n->next) {
        printf("%d ", n->value);
    }
    destroy(list);
    return 0;
}

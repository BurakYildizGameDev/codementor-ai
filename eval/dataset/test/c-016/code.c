#include <stdlib.h>

typedef struct {
    int *data;
    int size;
    int capacity;
} Stack;

void push(Stack *s, int value) {
    if (s->size == s->capacity) {
        s->capacity = s->capacity ? s->capacity * 2 : 4;
        s->data = realloc(s->data, s->capacity * sizeof(int));
    }
    s->data[s->size++] = value;
}

int pop(Stack *s) {
    return s->data[--s->size];
}

#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int *data;
    size_t size;
    size_t capacity;
} Stack;

int stack_push(Stack *s, int value) {
    if (s->size == s->capacity) {
        size_t new_cap = s->capacity ? s->capacity * 2 : 8;
        if (new_cap > SIZE_MAX / sizeof(int)) {
            return -1;
        }
        int *grown = realloc(s->data, new_cap * sizeof(int));
        if (grown == NULL) {
            return -1;
        }
        s->data = grown;
        s->capacity = new_cap;
    }
    *(s->data + s->size++) = value;
    return 0;
}

int stack_pop(Stack *s, int *out) {
    if (s->size == 0) {
        return -1;
    }
    *out = *(s->data + --s->size);
    return 0;
}

void stack_destroy(Stack *s) {
    free(s->data);
    memset(s, 0, sizeof *s);
}

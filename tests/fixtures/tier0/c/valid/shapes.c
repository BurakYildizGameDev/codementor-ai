#include <math.h>
#include <stdio.h>

#define PI 3.14159265358979
#define SQUARE(x) ((x) * (x))

typedef enum { CIRCLE, RECT } Kind;

typedef struct {
    Kind kind;
    union {
        struct { double r; } circle;
        struct { double w, h; } rect;
    } u;
} Shape;

typedef double (*AreaFn)(const Shape *);

static double circle_area(const Shape *s) { return PI * SQUARE(s->u.circle.r); }
static double rect_area(const Shape *s) { return s->u.rect.w * s->u.rect.h; }

static const AreaFn AREA[] = { [CIRCLE] = circle_area, [RECT] = rect_area };

int main(void) {
    Shape shapes[] = {
        { .kind = CIRCLE, .u.circle = { .r = 2.0 } },
        { .kind = RECT, .u.rect = { .w = 3.0, .h = 4.0 } },
    };
    double total = 0.0;
    for (size_t i = 0; i < sizeof shapes / sizeof shapes[0]; ++i) {
        total += AREA[shapes[i].kind](&shapes[i]);
    }
    printf("%.2f %.2f\n", total, sqrt(total));
    return 0;
}

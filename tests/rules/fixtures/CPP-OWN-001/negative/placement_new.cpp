#include <new>

struct Particle { float x = 0.f; };

void reset(void* storage) {
    Particle* p = new (storage) Particle();
    p->~Particle();
}

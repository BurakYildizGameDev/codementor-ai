#include <cstdint>

int64_t fast_power(int64_t base, int exp) {
    int64_t result = 1;
    int64_t current = base;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result *= current;
        }
        exp /= 2;
        if (exp > 0) {
            current *= current;
        }
    }
    return result;
}

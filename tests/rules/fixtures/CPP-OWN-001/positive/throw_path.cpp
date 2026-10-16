// EXPECT: 5, 8 · EXPECT_KIND: issue
#include <stdexcept>

void store(int n) {
    int* p = new int(n);
    if (n < 0) { throw std::runtime_error("negatif"); }
    *p += 1;
    delete p;
}

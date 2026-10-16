// EXPECT: 5, 8 · EXPECT_KIND: issue
#include <iostream>

int read_or_fail(bool ok) {
    int* value = new int(0);
    if (!ok) return -1;  // erken çıkış: `delete` atlanır
    std::cout << *value << "\n";
    delete value;
    return *value;
}

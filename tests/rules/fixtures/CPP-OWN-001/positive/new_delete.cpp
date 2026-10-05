// EXPECT: 6, 8 · EXPECT_KIND: suggestion
#include <iostream>

struct Enemy { int hp = 10; };
int main() {
    Enemy* e = new Enemy();
    std::cout << e->hp << "\n";
    delete e;
    return 0;
}

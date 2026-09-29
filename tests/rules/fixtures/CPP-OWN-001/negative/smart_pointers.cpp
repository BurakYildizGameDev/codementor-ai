#include <memory>

struct Enemy { int hp = 10; };

int main() {
    auto e = std::make_unique<Enemy>();
    std::shared_ptr<Enemy> boss = std::make_shared<Enemy>();
    return e->hp + boss->hp;
}

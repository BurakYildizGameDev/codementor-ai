#include <string>

class Player {
public:
    std::string name;
    int score = 0;
}

int main() {
    Player p;
    p.score = 10;
    return 0;
}

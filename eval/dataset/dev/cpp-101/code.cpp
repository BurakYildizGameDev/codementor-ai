#include <iostream>

struct Point {
    int x;
    int y;
}

int main() {
    Point p;
    p.x = 1;
    p.y = 2;
    std::cout << p.x << std::endl;
    return 0;
}

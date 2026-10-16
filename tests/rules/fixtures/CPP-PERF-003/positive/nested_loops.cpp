// EXPECT: 7, 8
#include <iostream>

void grid(int rows, int cols) {
    for (int r = 0; r < rows; ++r) {
        for (int c = 0; c < cols; ++c) {
            std::cout << r << c << std::endl;
            std::cout << std::endl;
        }
    }
}

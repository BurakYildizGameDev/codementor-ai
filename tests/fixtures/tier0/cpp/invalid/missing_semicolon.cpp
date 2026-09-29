#include <iostream>
#include <vector>

int main() {
    std::vector<int> values{1, 2, 3};
    int sum = 0;
    for (int v : values) {
        sum += v;
    }
    std::cout << sum << std::endl // expect-error
    return 0;
}

#include <map>
#include <string>

template <typename T>
T max_of(T a, T b) {
    return a > b ? a : b;
}

int main() {
    std::map<std::string, int> counts;
    counts["a"] = max_of<int>(1, 2);
    for (const auto& [key, value] : counts {  // expect-error
        (void)key;
    }
    return 0;
}

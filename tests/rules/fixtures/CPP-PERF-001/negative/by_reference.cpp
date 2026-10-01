#include <string>
#include <string_view>
#include <vector>

void prototype_only(std::vector<int> values);

int total(const std::vector<int>& values) {
    int s = 0;
    for (int v : values) s += v;
    return s;
}

size_t count(const std::vector<int>* values, std::string_view name, int n) {
    return values->size() + name.size() + n;
}

void consume(std::vector<int>&& values) {
    values.clear();
}

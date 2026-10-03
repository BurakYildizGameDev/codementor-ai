#include <iostream>
#include <string>
#include <vector>

void print_names(std::vector<std::string> names) {
    for (const auto& name : names) {
        std::cout << name << "\n";
    }
}

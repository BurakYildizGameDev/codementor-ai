// EXPECT: 10, 11 · EXPECT_KIND: suggestion
#include <iostream>

int status_of() {
    if (std::cin.fail()) return -1;  // başka kapsam: aşağıdaki `value` ile ilgisi yok
    return 0;
}

int main() {
    int* value = new int(7);
    delete value;  // eşleşiyor → öneri (hata değil)
    return *value;
}

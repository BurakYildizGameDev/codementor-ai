#include <iostream>

void process_buffer(int size) {
    int* data = new int[size];
    for (int i = 0; i < size; ++i) {
        data[i] = i * 2;
    }
    delete[] data;
}

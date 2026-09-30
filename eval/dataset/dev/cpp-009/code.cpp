#include <cstddef>
#include <cstring>

class Buffer {
public:
    explicit Buffer(std::size_t size) : size_(size), data_(new char[size]) {
        std::memset(data_, 0, size_);
    }
    ~Buffer() {
        delete[] data_;
    }
    char* data() { return data_; }
    std::size_t size() const { return size_; }

private:
    std::size_t size_;
    char* data_;
};

void fill(Buffer b, char c) {
    std::memset(b.data(), c, b.size());
}

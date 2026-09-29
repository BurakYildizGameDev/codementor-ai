#include <algorithm>
#include <cstddef>
#include <iostream>
#include <utility>

class Buffer {
public:
    explicit Buffer(std::size_t n = 0) : size_(n), data_(n ? new double[n]{} : nullptr) {}
    ~Buffer() { delete[] data_; }

    Buffer(const Buffer& other) : Buffer(other.size_) {
        std::copy(other.data_, other.data_ + size_, data_);
    }
    Buffer(Buffer&& other) noexcept
        : size_(std::exchange(other.size_, 0)), data_(std::exchange(other.data_, nullptr)) {}

    Buffer& operator=(Buffer other) noexcept {
        swap(*this, other);
        return *this;
    }

    friend void swap(Buffer& a, Buffer& b) noexcept {
        using std::swap;
        swap(a.size_, b.size_);
        swap(a.data_, b.data_);
    }

    double& operator[](std::size_t i) { return data_[i]; }
    [[nodiscard]] std::size_t size() const noexcept { return size_; }

private:
    std::size_t size_;
    double* data_;
};

int main() {
    Buffer a(3);
    a[0] = 1.5;
    Buffer b = a;
    Buffer c = std::move(a);
    std::cout << b[0] << ' ' << c.size() << '\n';
}

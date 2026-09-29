#include <vector>

class Buffer {
public:
    explicit Buffer(std::size_t n) : data_(n) {}
    Buffer(const Buffer&) = delete;
    Buffer& operator=(const Buffer&) = delete;
private:
    std::vector<int> data_;
};

#include <string>
#include <utility>
#include <vector>

class Widget {
public:
    explicit Widget(std::vector<int> data) : data_(std::move(data)) {}
    void set_name(std::string name) { name_ = std::move(name); }

private:
    std::vector<int> data_;
    std::string name_;
};

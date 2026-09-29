#include <memory>
#include <string>
#include <vector>

namespace fs {

class Node {
public:
    explicit Node(std::string name, Node* parent = nullptr)
        : name_(std::move(name)), parent_(parent) {}

    Node& add_child(const std::string& name) {
        children_.push_back(std::make_unique<Node>(name, this));
        return *children_.back();
    }

    [[nodiscard]] std::string path() const {
        if (parent_ == nullptr) {
            return "/" + name_;
        }
        return parent_->path() + "/" + name_;
    }

    template <typename Fn>
    void visit(Fn&& fn) const {
        fn(*this);
        for (const auto& child : children_) {
            child->visit(fn);
        }
    }

private:
    std::string name_;
    Node* parent_;
    std::vector<std::unique_ptr<Node>> children_;
};

}  // namespace fs

int main() {
    auto root = std::make_unique<fs::Node>("usr");
    root->add_child("local").add_child("bin");
    int count = 0;
    root->visit([&count](const fs::Node&) { ++count; });
    return count == 3 ? 0 : 1;
}

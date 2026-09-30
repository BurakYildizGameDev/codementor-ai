#include <memory>
#include <string>
#include <vector>

struct Node {
    std::string name;
    std::shared_ptr<Node> parent;
    std::vector<std::shared_ptr<Node>> children;
};

std::shared_ptr<Node> add_child(const std::shared_ptr<Node>& parent, const std::string& name) {
    auto child = std::make_shared<Node>();
    child->name = name;
    child->parent = parent;
    parent->children.push_back(child);
    return child;
}

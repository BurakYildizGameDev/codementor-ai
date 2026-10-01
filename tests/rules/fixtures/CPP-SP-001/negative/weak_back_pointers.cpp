#include <memory>
#include <vector>

struct Owner;

struct Pet {
    std::weak_ptr<Owner> owner;
};

struct Owner {
    std::shared_ptr<Pet> pet;
};

class TreeNode {
public:
    std::vector<std::shared_ptr<TreeNode>> children;
    std::weak_ptr<TreeNode> parent;
};

// EXPECT: 9
#include <memory>
#include <vector>

class TreeNode {
public:
    int value = 0;
    std::vector<std::shared_ptr<TreeNode>> children;
    std::shared_ptr<TreeNode> parent;
};

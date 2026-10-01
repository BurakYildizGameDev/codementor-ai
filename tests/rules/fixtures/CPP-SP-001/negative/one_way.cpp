#include <memory>

struct BinaryNode {
    int key;
    std::shared_ptr<BinaryNode> left;
    std::shared_ptr<BinaryNode> right;
};

struct ListNode {
    int value;
    std::shared_ptr<ListNode> next;
};

struct Engine {};

struct Car {
    std::shared_ptr<Engine> engine;
};

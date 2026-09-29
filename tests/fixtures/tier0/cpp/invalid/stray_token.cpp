#include <memory>

struct Node {
    int value = 0;
    std::unique_ptr<Node> next;
};

int length(const Node* head) {
    int n = 0;
    while (head != nullptr) {
        ++n;
        head = head->next.get() @; // expect-error
    }
    return n;
}

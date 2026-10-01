#include <functional>
#include <memory>

struct Node {
    std::shared_ptr<Node> fallback;
    std::shared_ptr<Node> preview;
    std::shared_ptr<Node> callback;
};

struct A;

struct B {
    std::function<void(std::shared_ptr<A>)> onDone;
};

struct A {
    std::shared_ptr<B> b;
};

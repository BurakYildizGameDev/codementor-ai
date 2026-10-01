// EXPECT: 8
#include <memory>
using namespace std;

struct Node {
    int value;
    shared_ptr<Node> next;
    shared_ptr<Node> prev;
};

#include <string>

class Greeter {
public:
    explicit Greeter(std::string name) : name_(std::move(name)) {}

    std::string greet() const {
        return "Merhaba, " + name_;
    }

private:
    std::string name_; // expect-error

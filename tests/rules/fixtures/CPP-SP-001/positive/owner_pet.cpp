// EXPECT: 7, 11
#include <memory>

struct Owner;

struct Pet {
    std::shared_ptr<Owner> owner;
};

struct Owner {
    std::shared_ptr<Pet> pet;
};

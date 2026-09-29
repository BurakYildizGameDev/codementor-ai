#include <list>
#include <optional>
#include <string>
#include <unordered_map>
#include <utility>

template <typename K, typename V>
class LruCache {
public:
    explicit LruCache(std::size_t capacity) : capacity_(capacity) {}

    std::optional<V> get(const K& key) {
        auto it = index_.find(key);
        if (it == index_.end()) {
            return std::nullopt;
        }
        order_.splice(order_.begin(), order_, it->second);
        return it->second->second;
    }

    void put(const K& key, V value) {
        if (capacity_ == 0) {
            return;
        }
        if (auto it = index_.find(key); it != index_.end()) {
            it->second->second = std::move(value);
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        if (order_.size() == capacity_) {
            index_.erase(order_.back().first);
            order_.pop_back();
        }
        order_.emplace_front(key, std::move(value));
        index_[key] = order_.begin();
    }

private:
    using Entry = std::pair<K, V>;
    std::size_t capacity_;
    std::list<Entry> order_;
    std::unordered_map<K, typename std::list<Entry>::iterator> index_;
};

int main() {
    LruCache<int, std::string> cache{2};
    cache.put(1, "bir");
    cache.put(2, "iki");
    cache.get(1);
    cache.put(3, "üç");
    return cache.get(2).has_value() ? 1 : 0;
}

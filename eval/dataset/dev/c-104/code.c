#include <stdbool.h>
#include <stddef.h>

bool is_palindrome(const char *s, size_t len) {
    if (len == 0) {
        return true;
    }
    size_t left = 0;
    size_t right = len - 1;
    while (left < right) {
        if (s[left] != s[right]) {
            return false;
        }
        left++;
        right--;
    }
    return true;
}

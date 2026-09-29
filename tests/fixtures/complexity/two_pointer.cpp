// expect-hint: n^2 | low
// Gerçek karmaşıklık O(n): j hiç geri gitmez. İç içe çarpım ipucu burada YANILIR;
// ipucu bunu sayaç sezgiseliyle fark edip düşük güven vermelidir (mimari §5.3.2).
#include <vector>

int longest_window(const std::vector<int>& a, int k) {
    int best = 0;
    size_t j = 0;
    for (size_t i = 0; i < a.size(); ++i) {
        while (j < a.size() && a[j] - a[i] <= k) {
            ++j;
        }
        best = std::max(best, static_cast<int>(j - i));
    }
    return best;
}

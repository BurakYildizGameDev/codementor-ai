// EXPECT: 9, 16
#include <map>
#include <string>
#include <vector>
using namespace std;

class Board {
public:
    int best(map<string, int> scores, int floor) const {
        int b = floor;
        for (const auto& kv : scores) if (kv.second > b) b = kv.second;
        return b;
    }
};

int cells(vector<vector<int>> grid) {
    return static_cast<int>(grid.size());
}

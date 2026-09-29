// expect-hint: n^2 | high
int count_pairs(const int *a, int n, int target) {
    int pairs = 0;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            if (a[i] + a[j] == target) {
                pairs++;
            }
        }
    }
    return pairs;
}

// expect-hint: 1 | high
int first_plus_last(const int *a, int n) {
    int total = a[0] + a[n - 1];
    for (int i = 0; i < 4; i++) {
        total += i;
    }
    return total;
}

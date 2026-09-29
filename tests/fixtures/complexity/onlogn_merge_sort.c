// expect-hint: n log n | low
void merge(int *a, int *tmp, int lo, int mid, int hi) {
    int i = lo, j = mid + 1, k = lo;
    while (i <= mid && j <= hi) {
        tmp[k++] = a[i] <= a[j] ? a[i++] : a[j++];
    }
    while (i <= mid) { tmp[k++] = a[i++]; }
    while (j <= hi) { tmp[k++] = a[j++]; }
    for (k = lo; k <= hi; k++) { a[k] = tmp[k]; }
}

void merge_sort(int *a, int *tmp, int lo, int hi) {
    if (lo >= hi) {
        return;
    }
    int mid = lo + (hi - lo) / 2;
    merge_sort(a, tmp, lo, mid);
    merge_sort(a, tmp, mid + 1, hi);
    merge(a, tmp, lo, mid, hi);
}

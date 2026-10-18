// EXPECT: 4, 6 · EXPECT_KIND: issue
void f(int n) {
    for (int i = 0; i < n; ++i) {
        int* p = new int(i);
        if (i > 3) { continue; }
        delete p;
    }
}

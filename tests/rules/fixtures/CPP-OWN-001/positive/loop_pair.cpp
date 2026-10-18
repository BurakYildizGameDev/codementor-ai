// EXPECT: 4, 5 · EXPECT_KIND: suggestion
void f(int n) {
    for (int i = 0; i < n; ++i) {
        int* p = new int(i);
        delete p;
    }
}

// EXPECT: 4, 5, 6, 7 · EXPECT_KIND: suggestion
void f(int n) {
    if (n < 0) { return; }
    int* a = new int(n);
    delete a;
    int* b = new int(n);
    delete b;
    return;
}

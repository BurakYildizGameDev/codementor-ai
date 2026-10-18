// EXPECT: 3, 5 · EXPECT_KIND: issue
void f(int n) {
    int* p = new int(n);
    { if (n) { return; } }
    delete p;
}

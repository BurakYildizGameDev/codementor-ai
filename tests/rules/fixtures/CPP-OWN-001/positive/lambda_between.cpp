// EXPECT: 3, 6 · EXPECT_KIND: suggestion
void apply(int n) {
    int* p = new int(n);
    auto pick = [](int x) { if (x > 0) { return 1; } return 0; };
    *p = pick(n);
    delete p;
}

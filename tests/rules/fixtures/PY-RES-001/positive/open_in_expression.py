# EXPECT: 3, 7 · EXPECT_KIND: issue
def count_lines(path):
    return len(open(path).readlines())


def write(path, text):
    handle = open(path, "w", encoding="utf-8")
    handle.write(text)

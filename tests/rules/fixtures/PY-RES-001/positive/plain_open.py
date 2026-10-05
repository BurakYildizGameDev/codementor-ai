# EXPECT: 3 · EXPECT_KIND: suggestion
def first_line(path):
    f = open(path)
    line = f.readline()
    f.close()
    return line

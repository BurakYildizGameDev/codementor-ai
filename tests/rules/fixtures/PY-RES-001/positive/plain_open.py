# EXPECT: 3
def first_line(path):
    f = open(path)
    line = f.readline()
    f.close()
    return line

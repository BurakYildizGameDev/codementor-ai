def first_line(path):
    with open(path, encoding="utf-8") as f:
        return f.readline()

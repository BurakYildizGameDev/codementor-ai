def count_file_lines(filename: str) -> int:
    f = open(filename, "r", encoding="utf-8")
    count = 0
    for line in f:
        count += 1
    f.close()
    return count

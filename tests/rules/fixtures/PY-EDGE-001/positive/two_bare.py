# EXPECT: 6, 13
def load(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except:
        pass


def save(path, data):
    try:
        Path(path).write_text(data)
    except:  # sessizce yut
        print("hata")

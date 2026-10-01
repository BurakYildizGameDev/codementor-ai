# EXPECT: 5
def parse(text):
    try:
        return int(text)
    except:
        return 0

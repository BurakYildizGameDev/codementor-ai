def word_count(text):
    seen = []
    result = {}
    for word in text.lower().split():
        if word not in seen:
            seen.append(word)
            result[word] = 0
        result[word] += 1
    return result

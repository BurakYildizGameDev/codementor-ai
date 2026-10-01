def greet(name="dünya", times: int = 1, parts=()):
    return [f"Merhaba {name}"] * times + list(parts)

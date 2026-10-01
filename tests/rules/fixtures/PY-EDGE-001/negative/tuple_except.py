def read(path):
    try:
        with open(path) as f:
            return f.read()
    except (OSError, UnicodeDecodeError) as exc:
        raise RuntimeError(path) from exc

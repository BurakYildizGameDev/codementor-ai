def add_item(item, bucket=[]):
    if item == None:
        return bucket
    bucket.append(item)
    return bucket

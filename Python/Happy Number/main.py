def is_happy(n):
    hash = []
    digits=[int(x) for x in str(n)]
    result = sum([digit*digit for digit in digits])
    while result != 1:
        if result in hash:
            return False 
        hash.append(result)
        digits=[int(x) for x in str(result)]
        result = sum([digit*digit for digit in digits])
    return True

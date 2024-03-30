# 1 <= s.length <= 15
# s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M')
# It is guaranteed that s is a valid roman numeral in the range [1, 3999].

DICTIONARY = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L":50,
    "C":100,
    "D": 500,
    "M": 1000
}

def convert(s: str) -> int:
    sum = 0
    i = 0
    while i < len(s):
        print(sum)
        if s[i] == "I" and i+1 < len(s):
            if s[i+1] == "V" or s[i+1] == "X":
                sum = sum + DICTIONARY[s[i+1]]-DICTIONARY[s[i]]
                i+=2
                continue
            sum = sum + DICTIONARY[s[i]]
            i+=1
            continue
        if s[i] == "X" and i+1 < len(s):
            if s[i+1] == "L" or s[i+1] == "C":
                sum = sum + DICTIONARY[s[i+1]]-DICTIONARY[s[i]]
                i+=2
                continue
            sum = sum + DICTIONARY[s[i]]
            i+=1
            continue
        if s[i] == "C" and i+1 < len(s):
            if s[i+1] == "D" or s[i+1] == "M":
                sum = sum + DICTIONARY[s[i+1]]-DICTIONARY[s[i]]
                i+=2
                continue
            sum = sum + DICTIONARY[s[i]]
            i+=1
            continue
        else:
            sum = sum + DICTIONARY[s[i]]
            i+=1
    return sum

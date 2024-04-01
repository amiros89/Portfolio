# Given two strings ransomNote and magazine, returns true if ransomNote can be constructed by using the letters from magazine and false otherwise.

# Each letter in magazine can only be used once in ransomNote.

 

# Constraints:

# 1 <= ransomNote.length, magazine.length <= 105
# ransomNote and magazine consist of lowercase English letters.


# Helper method
def create_hash(s:str) -> dict:
    hash = {}
    for char in s:
        if char in hash:
            hash[char] += 1
        else:
            hash[char] = 1
    return hash

# Main solution
def can_construct(ransom_note: str,magazine:str) -> bool:
    ransom_note_hash = create_hash(ransom_note)
    magazine_hash = create_hash(magazine)
    for key,value in ransom_note_hash.items():
        if key not in magazine_hash.keys():
            return False
        if magazine_hash[key]<value:
            return False
    return True
 
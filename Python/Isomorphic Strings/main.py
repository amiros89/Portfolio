# Given two strings s and t, determines if they are isomorphic.

# Two strings s and t are isomorphic if the characters in s can be replaced to get t.

# All occurrences of a character must be replaced with another character while preserving the order of characters.
# No two characters may map to the same character, but a character may map to itself.
# 1 <= s.length <= 5 * 104
# t.length == s.length
# s and t consist of any valid ascii character.

def create_index_map(s: str) -> dict:
    index_map = {}
    for i, char in enumerate(s):
        if char in index_map:
            index_map[char].append(i)
        else:
            index_map[char] = [i]
    return index_map

def is_ismorphic(s:str,t:str) -> bool:
    s_index_map = create_index_map(s)
    t_index_map = create_index_map(t)
    return [*s_index_map.values()] == [*t_index_map.values()]


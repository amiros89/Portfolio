from typing import List


class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        common_prefix = ""
        shortest_word = min(strs, key=len)
        chars_match = True
        for i, char in enumerate(
            shortest_word
        ):  # longest common prefix can only be as long as the shortest word
            for str in strs:  # for each word
                if str[i] != char:
                    chars_match = False
                    break
            if chars_match:
                common_prefix += char
            else:
                break
        return common_prefix

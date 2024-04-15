# You are given a 0-indexed string word, consisting of lowercase English letters. You need to select one index and remove the letter at that index from word so that the frequency of every letter present in word is equal.

# Return true if it is possible to remove one letter so that the frequency of all letters in word are equal, and false otherwise.

# Note:

# The frequency of a letter x is the number of times it occurs in the string.
# You must remove exactly one letter and cannot choose to do nothing.

# 2 <= word.length <= 100
# word consists of lowercase English letters only.


from typing import List

class Solution:
    def get_frequencies(self,word:str) -> List:
        frequencies = {}
        for char in word:
            if char in frequencies:
                frequencies[char]+=1
            else:
                frequencies[char] = 1
        return [*frequencies.values()]
    
    def frequencies_equal(self,frequencies:List) -> bool:
        init = frequencies[0]
        for freq in frequencies[1::]:
            if freq != init:
                return False
        return True
    
    def equalFrequency(self, word: str) -> bool:
        chars_list = list(word)
        all_frequencies_equal = False
        for i in range(len(chars_list)):
            new_word=chars_list[0:i]+chars_list[i+1::]
            if self.frequencies_equal(self.get_frequencies(new_word)):
                all_frequencies_equal = True
        return all_frequencies_equal

    
# Given a string s consisting of words and spaces, returns the length of the last word in the string.

# A word is a maximal 
# substring
#  consisting of non-space characters only.

def length_of_last_word(s: str) -> int:
    word_array = s.split(" ")
    for word in word_array[::-1]:
        if word.isalnum():
            last_word = word
            break
    return len(last_word)


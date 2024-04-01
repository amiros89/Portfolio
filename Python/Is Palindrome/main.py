# A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.

# Given a string s, returns true if it is a palindrome, or false otherwise.
import re

def lower_remove_non_alphanumeric(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string).lower()

def is_palindrome(s:str) -> bool:
    return lower_remove_non_alphanumeric(s) == lower_remove_non_alphanumeric(s[::-1])
    

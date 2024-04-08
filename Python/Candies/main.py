# Alice has n candies, where the ith candy is of type candyType[i]. Alice noticed that she started to gain weight, so she visited a doctor.

# The doctor advised Alice to only eat n / 2 of the candies she has (n is always even). Alice likes her candies very much, and she wants to eat the maximum number of different types of candies while still following the doctor's advice.

# Given the integer array candyType of length n, return the maximum number of different types of candies she can eat if she only eats n / 2 of them.

# Constraints:

# n == candyType.length
# 2 <= n <= 104
# n is even.
# -105 <= candyType[i] <= 105


from typing import List

class Solution:
    def distributeCandies(self, candyType: List[int]) -> int:
        return min(int(len(candyType)/2),len(set(candyType)))


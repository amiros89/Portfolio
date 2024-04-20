# You are given an integer array nums. A subsequence of nums is called a square streak if:

# The length of the subsequence is at least 2, and
# after sorting the subsequence, each element (except the first element) is the square of the previous number.
# Return the length of the longest square streak in nums, or return -1 if there is no square streak.

# A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

# 2 <= nums.length <= 105
# 2 <= nums[i] <= 105

from typing import List

class Solution:

    def longestSquareStreak(self, nums: List[int]) -> int:
        max_streak = -1
        set_of_nums = set(nums)
        for num in set_of_nums:
            current_streak = 1
            base = num
            powers = [pow(base, pow(2,i)) for i in range(1,5)]
            for power in powers:
                if power in set_of_nums:
                    current_streak += 1
                else:
                    break
            if current_streak > 1 and current_streak > max_streak:
                max_streak = current_streak
            if max_streak == 5:
                return max_streak
        return max_streak        


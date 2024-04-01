# You are given a sorted unique integer array nums.

# A range [a,b] is the set of all integers from a to b (inclusive).

# Return the smallest sorted list of ranges that cover all the nums in the array exactly. That is, each element of nums is covered by exactly one of the ranges, and there is no integer x such that x is in one of the ranges but not in nums.

# Each range [a,b] in the list should be output as:

# "a->b" if a != b
# "a" if a == b

# Constraints:

# 0 <= nums.length <= 20
# -231 <= nums[i] <= 231 - 1
# All the values of nums are unique.
# nums is sorted in ascending order.

from typing import List

def summary_ranges(nums: List[int]) ->List[str]:
    splits = []
    ranges = []
    if nums:
        current_split = [nums[0]]

        for i in range(1, len(nums)):
            if nums[i] - nums[i - 1] != 1:
                splits.append(current_split)
                current_split = [nums[i]]
            else:
                current_split.append(nums[i])

        splits.append(current_split)
        for split in splits:
            if len(split)==1:
                ranges.append(f"{split[0]}")
            else:
                ranges.append(f"{split[0]}->{split[-1]}")   
    return ranges

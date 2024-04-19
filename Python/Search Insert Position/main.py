from typing import List

class Solution:
    def binarySearch(self,nums: List[int],target: int,left: int, right: int) -> int:
        mid_index = (left+right)//2
        if right<left:
                return left
        middle_num = nums[mid_index]
        if middle_num==target:
            return mid_index
        elif middle_num > target:
            return self.binarySearch(nums,target,left=left,right=mid_index-1)
        else:
            return self.binarySearch(nums,target,left=mid_index+1,right=right)    

    def searchInsert(self, nums: List[int], target: int) -> int:
        if not nums:
            return 0
        if target > nums[len(nums)-1]:
            return len(nums)
        if target < nums[0]:
            return 0
        return self.binarySearch(nums,target,left=0,right=len(nums))

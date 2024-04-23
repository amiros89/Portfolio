from typing import List


class Solution:
    def recFindPeakElement(self,nums,left,right) -> int: 
        if left == right:
            return left
        mid = (left+right)//2
        if nums[mid] > nums[mid+1]:
            return self.recFindPeakElement(nums,left,mid)
        else:
            return self.recFindPeakElement(nums,mid+1,right)

    
    def findPeakElement(self, nums: List[int]) -> int:
        return self.recFindPeakElement(nums,left=0,right=len(nums)-1)
        
nums = [7,5,4]
sol = Solution().findPeakElement(nums)
print(sol)
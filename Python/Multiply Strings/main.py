class Solution:
    digits = {
        "0": 0,
        "1" :1,
        "2" :2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9":9
    }  

    
    def multiply(self, num1: str, num2: str) -> str:
        numeric_num1 = 0
        numeric_num2 = 0
        for i,digit in enumerate(num1):
            numeric_num1 += (self.digits[digit])*pow(10,len(num1)-i-1)
        for j,digit in enumerate(num2):
            numeric_num2 += (self.digits[digit])*pow(10,len(num2)-j-1)
        return str(numeric_num1*numeric_num2)
        
        
        
        
num1 = "4"
num2 = "3"
sol = Solution().multiply(num1,num2)
print(sol)
from typing import List

class Solution:
    def isRowOrColumnValid(self,row:List[str]) -> bool:
        for num in row:
            if num == '.':
                continue
            if row.count(num) > 1:
                return False
        return True
    
    def isSubBoxValid(self,sub_box:List[List[str]]) -> bool:
        flat_sub_box = []
        for row in sub_box:
            flat_sub_box.extend(row)                
        return self.isRowOrColumnValid(flat_sub_box)
    
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        for i in range(len(board)):
            if not self.isRowOrColumnValid(board[i]):
                return False
        for i in range(len(board)):
            column = [row[i] for row in board[0:len(board)]]
            if not self.isRowOrColumnValid(column):
                return False
        submatrices = []
        for i in [0, 3, 6]:  # top left, middle, bottom left
            for j in [0, 3, 6]:  # top left, middle, bottom right
                submatrix = [row[j:j+3] for row in board[i:i+3]]
                submatrices.append(submatrix)
        for i in range(0,9):
            if not self.isSubBoxValid(submatrices[i]):
                return False     
        return True


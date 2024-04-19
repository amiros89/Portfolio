from typing import List,Optional

# You are given the heads of two sorted linked lists list1 and list2.

# Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

# Return the head of the merged linked list.

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        linked_list = []
        while list1 and list2:
            node = ListNode()
            linked_list.append(node)
            if list1.val < list2.val:
                node.val = list1.val
                node.next = list1
                list1 = list1.next
            else:
                node.val = list2.val
                node.next = list2.next
                list2=list2.next
        while list1:
            node = ListNode()
            linked_list.append(node)
            node.val = list1.val
            node.next = list1.next
            list1 = list1.next
        while list2:
            node = ListNode()
            linked_list.append(node)
            node.val = list2.val
            if list2.next:
                node.next = list2.next
            list2 = list2.next

        for i in range(len(linked_list)-1):
            linked_list[i].next = linked_list[i+1]
        if linked_list:
            return linked_list[0]

    
list1_node3=ListNode(4)
list1_node2=ListNode(3,list1_node3)
list1 = ListNode(1,list1_node2)

list2_node3=ListNode(5)
list2_node2=ListNode(2,list2_node3)
list2=ListNode(2,list2_node2)



# list1 = [1,2,4]
# list2 = [1,3,4]

# list1 = []
# # list2 = []

sol = Solution().mergeTwoLists(list1,list2)
# print(sol)
print("actual linked list")
while sol:
    print(sol.val)
    sol = sol.next
    # sol = sol.next
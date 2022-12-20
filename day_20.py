from typing import Any, Optional, Self
from utils import read_input

inpt = read_input("20")

class Node:
    def __init__(self, item, next_node=None):
        self.item: Any = item
        self.next: Optional[Self] = next_node

class LoopedList:
    def __init__(self):
        self.start: Optional[Node] = None
        self.length = 0

    @classmethod
    def from_list(cls, items: list[Any]) -> Self:
        l = LoopedList()
        for item in items:
            l.append(item)
        return l

    def __len__(self):
        return self.length

    def append(self, item: Any):
        if self.start is None:
            if isinstance(item, Node):
                self.start = item
                self.start.next = self.start
            else:
                self.start = Node(item)
                self.start.next = self.start
        else:
            current = self.start
            while (current.next is not self.start):
                current = current.next
            if isinstance(item, Node):
                current.next = item
                item.next = self.start
            else:
                current.next = Node(item, next_node=self.start)
        self.length += 1

    def get(self, idx: int) -> Any:
        current = self.start
        for _ in range(idx):
            current = current.next
        return current.item

    def move(self, idx_from: int, steps: int) -> None:

        #Iterate to node before idx_from
        current = self.start
        for _ in range((idx_from - 1)%len(self)):
            current = current.next

        #Extract node to move and stich together adjacent nodes
        node_to_move = current.next
        if node_to_move == self.start:
            self.start = node_to_move.next
        current.next = node_to_move.next

        #Iterate to node before insertion
        for _ in range(steps):
            current = current.next

        node_to_move.next = current.next
        current.next = node_to_move


    def find_node_idx(self, node: Node) -> int:
        if self.start is None:
            return -1
        else:
            i = 0
            current = self.start
            if current is node:
                return i
            while (current.next is not self.start):
                current = current.next
                i+=1
                if current is node:
                    return i

        return -1

    def find_item_idx(self, item: any) -> int:
        if self.start is not None:
            i = 0
            current = self.start
            while (current.next is not self.start):
                if current.item == item:
                    return i
                current = current.next
                i+=1
        return -1

def solve(items: list[int], n: int = 1) -> int:
    #Pre-created nodes in a list means we can loop over the nodes in 
    #creation order by looping over this list
    items = [Node(item) for item in items]

    l = LoopedList.from_list(items)

    for _ in range(n):
        for item in items:
            if (current_idx := l.find_node_idx(item)) != -1:
                steps = item.item
                if steps > 0:
                    l.move(current_idx, steps % (len(l) - 1))
                elif steps < 0:
                    l.move(current_idx, (len(l) + steps - 1) % (len(l) - 1))

    return sum([
        l.get((1000 + l.find_item_idx(0))%len(l)), 
        l.get((2000 + l.find_item_idx(0))%len(l)), 
        l.get((3000 + l.find_item_idx(0))%len(l))
    ])

def test_solution():
    items = [1, 2, -3, 3, -2, 0, 4]
    return solve(items)

def get_first_solution():
    items = [int(x) for x in inpt]
    return solve(items)

def get_second_solution():
    items = [int(x)*811589153 for x in inpt]
    return solve(items, n=10)
    
print(test_solution())
print(get_first_solution())
print(get_second_solution())

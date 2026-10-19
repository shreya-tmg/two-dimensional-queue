#Two Dimensional Queues
#Shreya Tamang

class TwoDimensionalQ:
    def __init__(self, n: int = 4):
        # starter code
        # empty seats n * n grid / 2D grid (lists of lists)
        self._underlying: list[list[str]] = [[None for _ in range(n)] for _ in range(n)]

       # grid size
        self._n: int = n
       
        self._capacity: int = n * n
        self._usage: int = 0

        self._front_row: int = 0
        self._front_col: int = 0

        self._back_row: int = 0
        self._back_col: int = 0


    def get_capacity(self) -> int:
        return self._capacity

    
    def get_usage(self) -> int:
        return self._usage


    # moves to the next seat in line in row major order
    def advance(self, row: int, col: int) -> tuple[int, int]:
        col += 1
        # if we reach the end of this row, warp back to beginning 
        if col == self._n:
            col = 0
            row = (row + 1) % self._n
        return row, col


    def enqueue(self, value: str) -> bool:
        # check if there is space for another person
        success: bool = self._usage < self._capacity

        if success:
            # put new person in the seat where the back pointer is currently pointing
            # access back potiners seat position, places new person
            self._underlying[self._back_row][self._back_col] = value
            # then move back pointer forward to next available seat
            self._back_row, self._back_col = self.advance(self._back_row, self._back_col)
            self._usage += 1
        return success


    def dequeue(self) -> str | None:
        result: str | None = None

        # only remove someone if theres atleast one person in the queue
        if self._usage > 0:
            r, c = self._front_row, self._front_col
            #grab the person at the front ([r][c]seat holds the next person to be served)
            result = self._underlying[r][c]
            # remove person from seat
            self._underlying[r][c] = None
            # moves pointer to next person in line
            self._front_row, self._front_col = self.advance(r, c)
            self._usage -= 1
        return result


    def peek(self) -> str | None:
        value: str | None = None

        if self._usage > 0:
            # read who is in front (without removing them)
            value = self._underlying[self._front_row][self._front_col]
        return value


    def list_queue(self) -> list[str]:
        items: list[str] = []
        r, c = self._front_row, self._front_col

        # go through each person waiting
        for _ in range(self._usage):
            val = self._underlying[r][c]
            items.append(val)
            # move to next person in line
            r, c = self.advance(r, c)
        return items


    def __repr__(self) -> str:
        # show queue status when printing the object
        # returns more readable string information 
        return f"TwoDimensionalQ(usage={self._usage}/{self._capacity})"


    def __bool__(self) -> bool:
        # return True if people are waiting, False if empty
        # converts your queue into a simple True/False
        return self._usage > 0


# TESTING
if __name__ == "__main__":
    print("=== Two Dimensional Q Tests ===")

    # create 2x2 waiting room (so 4 total seats) for testing
    q = TwoDimensionalQ(2)
    
    # test 1: check that empty queue works
    print("1. Empty queue:")
    print(f"{q.list_queue()}, usage={q.get_usage()}")
    assert q.get_usage() == 0 and not q
    
    # test 2: fill the queue completely
    print("\n2. Fill queue:")
    for name in ["Alice", "Bob", "Cathy", "Derek"]:
        q.enqueue(name)
        print(f"+{name}: {q.list_queue()}")
    assert q.get_usage() == 4
    # calls q.enqueue("Extra")
    assert not q.enqueue("Extra")  #full
    
    # test 3: FIFO order
    print("\n3. FIFO order:")
    print(f"Peek: {q.peek()}, Dequeue: {q.dequeue()}")
    print(f"Dequeue: {q.dequeue()}")
    print(f"Remaining: {q.list_queue()}")
    assert q.list_queue() == ["Cathy", "Derek"]

    # test 4: wrap-around
    print("\n4. Wrap-around:")
    print(f"Before wrap: {q.list_queue()}")
    q.enqueue("Eva")
    q.enqueue("Finn")
    print(f"After wrap: {q.list_queue()}")
    
    # test 5: empty the queue completely
    print("\n5. Empty queue:")
    while q:
        print(f"Dequeued: {q.dequeue()}")
    print(f"Final: usage={q.get_usage()}, empty? {not q}")
    assert q.get_usage() == 0 and not q

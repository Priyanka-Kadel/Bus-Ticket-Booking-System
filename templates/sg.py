class queue:
    def __init__(self) -> None:
        self.item=[]
        self.rare=None
        self.front=None
    def isEmpty(self):
        return len(self.item)==0
    def inqueue(self,data):
        self.item.append(data)
    def dequeue(self):
        if not self.isEmpty():
          return self.item.pop(0)
        else:
            print("empty")
    def peek(self):
        if not self.isEmpty():
            return self.item[0]
        else:
            print("empty")
    def size(self):
        return len(self.item)
s=queue()
s.inqueue(1)
s.inqueue(2)
s.inqueue(3)
s.inqueue(4)
s.inqueue(5)
print(s.item)
s.dequeue()
print(s.item)
print(s.peek())
s.size()



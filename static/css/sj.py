import heapq

class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def closestValues(root, k, x):
    result = []
    stack = []
    heapq.heapify(result)

    # In-order traversal
    while root or stack:
        while root:
            stack.append(root)
            root = root.left

        root = stack.pop()
        
        # Add the current value to the heap
        heapq.heappush(result, (abs(root.val - k), root.val))

        # If the heap size exceeds x, pop the smallest element
        if len(result) > x:
            heapq.heappop(result)

        root = root.right

    # Extract the values from the heap
    closest_values = [val for diff, val in sorted(result, key=lambda x: x[0])]

    return closest_values

# Example usage:
# Construct the binary search tree
root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(5)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)

# Input values
k = 3.8
x = 2

# Get the closest x values to the target k
output = closestValues(root, k, x)

print("Output:", output)

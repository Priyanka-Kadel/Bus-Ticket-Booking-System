def find_secret_recipients(n, intervals, first_person):
    graph = [[] for _ in range(n)]
    visited = set()

    # Build the graph
    for start, end in intervals:
        for i in range(start, end + 1):
            graph[first_person].append(i)

    # DFS function
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in graph[node]:
            dfs(neighbor)

    # Start DFS from the initial person
    dfs(first_person)

    return sorted(list(visited))

# Example usage:
n = 5
intervals = [(0, 2), (1, 3), (2, 4)]
first_person = 0
result = find_secret_recipients(n, intervals, first_person)
print(result)

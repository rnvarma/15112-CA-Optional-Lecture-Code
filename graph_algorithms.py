graph = {'A': set(['B', 'C']),
         'B': set(['A', 'D', 'E']),
         'C': set(['A', 'F']),
         'D': set(['B']),
         'E': set(['B', 'F']),
         'F': set(['C', 'E'])}

def dfs(graph, start):
    visited, stack = [], [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            stack.extend([x for x in graph[vertex] if x not in visited])
    return visited

def dfs_rec(graph,start,path = []):
    path = path + [start]
    for neighbor in graph[start]:
        if neighbor not in path:
            path = dfs_rec(graph, neighbor, path)
    return path

print (dfs(graph, 'A')) # {'E', 'D', 'F', 'A', 'C', 'B'}
print (dfs_rec(graph,'A'))

graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'F'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['C', 'E']}

def dfs_search(graph, start, node, path = []):
    path = path + [start]
    if (start == node):
        return path
    for neighbor in graph[start]:
        if neighbor not in path:
            newPath = dfs_search(graph, neighbor, node, path)
            if newPath != None:
                return newPath
    return None

print (dfs_search(graph, 'A', 'C'))

def bfs(graph, start):
    visited, queue = [], [start]
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.append(vertex)
            queue.extend([x for x in graph[vertex] if x not in visited])
    return visited

print (bfs(graph, 'A')) # {'B', 'C', 'A', 'F', 'D', 'E'}
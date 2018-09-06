
n = int(input())

graph = {}

for i in range(n):
    l, r = input().strip().split()
    if l in graph:
        graph[l].append(r)
    else:
        graph[l] = [r]






n, k, t = map(lambda x: int(x), input().strip().split(' '))
num = input().strip().split(' ')
num_count = {n: 0 for n in num}

q = {}

for i in range(1, n+1):
    num_count[num[i-1]] += 1
    l = i
    for j in range(i+1, n+1):
        r = j
        if r-l+1 == k:
            if not l in q:
                q[l] = []
            q[l].append(r)

res = 0

for i in num_count:
    if num.index(i) in q:
        if q[num.index(i)][-1]-num.index(i) >= t:
            res += q[num.index(i)][-1]-num.index(i)-t+1

print(res)

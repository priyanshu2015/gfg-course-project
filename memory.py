a = 2
b = 2
print(id(a))
print(id(b))
b = b + 2
print(id(b))
c = [1, 2, 3]
d = c
print(id(c))
print(id(d))
d.append(4)
print(c)
d = c.copy()
d.append(5)
print(d)
print(c)

e = [[1, 2, 3], [3, 4, 5]]
f = e.copy() # or copy(e)
f.append([5, 6, 7])
print(e)
print(f)
f[0].append(4)
print(e)
print(f)

import copy
f = copy.deepcopy(e)
f[0].append(5)
print(e)
print(f)

import numpy as np

x = np.array([[1, 2], [3, 7], [2, 12]])
y = np.array([1, 1])

v = x+y
w = np.empty_like(v)

for i in range(3):
    w[i, :] = v[i, :] + 1

# print(v)
# print("-"*20)
# print(w)
# print(x)
# print(np.sum(x))
# print(np.sum(x, axis=0))
# print(np.sum(x, axis=1))

a = (np.random.random_sample((2, 2, 2)))
print(a)

i = np.random.randint(5, size=(2, 2))

print(i)


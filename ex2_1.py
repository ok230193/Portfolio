from decimal import Decimal
a = 2e10
b = 3e-8
ans = 0.0
for i in range(10000000):
    ans += b
ans += a
print(ans)

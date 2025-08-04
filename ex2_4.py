from fractions import Fraction
a = Fraction(1, 6)
b = Fraction(5, 6)
ans = a * Fraction(1, 1 - b ** 3)
print(ans)

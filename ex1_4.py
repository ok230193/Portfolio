def search_three(x):
    three_i = 0
    for i, num in enumerate(x):
        if num % 3 == 0:
            three_i = i
    return three_i + 1


def main():
    aa = [1, 2, 3, 4, 5]
    print(f"3の倍数は{search_three(aa)}番目です")
    bb = [8, 2, 5, 3, 1]
    print(f"3の倍数は{search_three(bb)}番目です")
    cc = [6, 5, 7, 5, 2]
    print(f"3の倍数は{search_three(cc)}番目です")
    dd = [8, 9, 5, 1, 8]
    print(f"3の倍数は{search_three(dd)}番目です")


if __name__ == '__main__':
    main()

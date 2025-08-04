def main():
    h = [4, 5, 2, 9]
    sum = 1
    for i in range(4):
        sum += (2 ** (i+1) * h[i])
    print(sum)


if __name__ == '__main__':
    main()

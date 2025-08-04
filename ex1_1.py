def main():
    score_list = [3.4, 15.1, 9.07, 8.4, 43.0]
    sum_num = 0
    for score in score_list:
        sum_num += score
    average_num = sum_num / len(score_list)
    print(f'平均は{average_num}')


if __name__ == '__main__':
    main()

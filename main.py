while True:
    print('========================')
    print('나만의 퀴즈 게임')
    print('========================')
    print('1. 퀴즈 풀기')
    print('2. 퀴즈 추가')
    print('3. 퀴즈 목록')
    print('4. 점수 확인')
    print('5. 종료')
    print('========================')
    try:
        raw = input('선택 : ').strip()
        if raw == '':
            print('잘못된 입력입니다. [Enter]가 입력됨')
            continue
        opt = int(raw)
    except ValueError:
        print('잘못된 입력입니다. 숫자를 입력하세요.')
        continue
    except (KeyboardInterrupt, EOFError):
        print('잘못된 입력입니다. [Ctrl+C 또는 EOFError 발생]')
        break
    if 0 >= opt or opt >= 6:
        print('잘못된 입력입니다, 메뉴를 확인하고 다시 입력 해 주세요.')
        continue
    if opt == 1:
        print('퀴즈를 시작합니다.')
    elif opt == 2:
        print('퀴즈를 추가합니다')
    elif opt == 3:
        print('등록된 퀴즈 목록 (총 n개')
    elif opt == 4:
        print('최고 점수 : n점 (k문제 중 p개 정답)')
    elif opt == 5:
        print('종료')
        break
    else:
        print('잘못된 입력입니다.')
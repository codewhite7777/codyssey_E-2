import json

# ==========================================
# Quiz 클래스 정의
# ==========================================
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def quiz_display(self):
        print("문제 :", self.question)
        for i in range(len(self.choices)):
            print(f"  {i + 1}. {self.choices[i]}")

    def check_answer(self, user_answer):
        if self.answer == user_answer:
            return True
        return False

# ==========================================
# Default Quiz / state.json 로드 불가시 사용
# ========================================== 
default_quiz = [
    Quiz("볼링 한 게임은 몇 프레임으로 구성되어 있는가?", ["8프레임", "10프레임", "12프레임", "15프레임"], 2),
    Quiz("모든 핀을 첫 번째 투구에서 쓰러뜨리는 것을 무엇이라 하는가?",["스페어", "스트라이크", "거터", "터키"],2),
    Quiz("볼링 핀은 총 몇 개인가?",["8개", "10개", "12개", "15개"],2),
    Quiz("3연속 스트라이크를 무엇이라 부르는가?",["더블", "터키", "트리플", "햄본"],2),
    Quiz("볼링의 최고 점수(퍼펙트 게임)는 몇 점인가?",["200점", "250점", "280점", "300점"],4)
]

# ==========================================
# Quiz의 객체 리스트
# ========================================== 
quizzes = []

# ==========================================
# state.json에서 퀴즈 데이터 불러오기
# ==========================================
try:
    with open("state.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        # ==========================================
        # 데이터 정상 로드 시, 파일 -> 객체 변환 작업을 진행
        # 퀴즈 데이터 역직렬화 (deserialization)
        # ==========================================
        for item in data["quizzes"]:
            q = Quiz(item["question"],item["choices"], item["answer"])
            quizzes.append(q)
except FileNotFoundError:
        print("파일이 존재하지 않습니다, 기본 퀴즈로 진행합니다.")
        quizzes = default_quiz
except json.JSONDecodeError:
        print("파일 변환에 실패하였습니다, 기본 퀴즈로 진행합니다.")
        quizzes = default_quiz


#게임 종료 플래그
is_exit = False

# ==========================================
# 메인 메뉴 루프
# ==========================================
while True:
    if is_exit == True:
        break
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
        print('프로그램을 종료합니다. [Ctrl+C 또는 EOFError 발생]')
        break
    if 0 >= opt or opt > 5:
        print('잘못된 입력입니다, 메뉴를 확인하고 다시 입력 해 주세요.')
        continue
    if opt == 1:
        # 퀴즈가 없는 경우의 처리 
        if len(quizzes) == 0:
            print('등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가 해 주세요.')
            continue;
        print(f'퀴즈를 시작합니다. 총 {len(quizzes)}문제')
        print('============================')
        #점수 초기화
        score = 0
        #문제 출력
        for i in range(len(quizzes)):
            if is_exit == True:
                break
            print(f'[문제 {i+1}]')
            print(f'{quizzes[i].question}')
            for j in range(len(quizzes[i].choices)):
                print(f'{j+1}. {quizzes[i].choices[j]}')
        #사용자의 입력 검증
            while True:
                try:
                    user_raw_answer = input('정답 입력 : ').strip()
                    #공백 입력
                    if user_raw_answer == '':
                        print('잘못된 입력입니다. [Enter]가 입력됨')
                        continue
                    user_answer = int(user_raw_answer)
                    #선택지 외 입력
                    if user_answer < 1 or user_answer > len(quizzes[i].choices):
                        print('잘못된 입력입니다. 범위 내 선택지를 입력 하세요.')
                        continue
                    #정답 검증
                    if quizzes[i].check_answer(user_answer):
                        print('정답입니다.')
                        score += 1
                    else:
                        print('오답입니다.')
                    break
                #숫자가 아닌 값 입력
                except ValueError:
                    print('잘못된 입력입니다. 숫자를 입력하세요.')
                    continue
                #시그널 입력
                except (KeyboardInterrupt, EOFError):
                    print('프로그램을 종료합니다. [Ctrl+C 또는 EOFError 발생]')
                    is_exit = True
                    break
        #문제 풀이 후 스코어 및 정답 개수 처리
        if not is_exit:
            print(f'{len(quizzes)}문제 중 {score}문제 정답!')
        
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
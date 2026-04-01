import json

# ==========================================
# Quiz 클래스 정의
# ==========================================
class	Quiz:
	def	__init__(self, question, choices, answer):
		self.question = question
		self.choices = choices
		self.answer = answer

	def	quiz_display(self):
		print("문제 :", self.question)
		for i in range(len(self.choices)):
			print(f"  {i + 1}. {self.choices[i]}")

	def	check_answer(self, user_answer):
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
# QuizGame 클래스 정의
# ==========================================
class	QuizGame:
	# ==========================================
	# initializer
	# ==========================================
	def	__init__(self):
		self.quizzes = []
		self.best_score = None
		self.is_exit = False
		self.load_data()

	# ==========================================
	# 데이터 로드 메서드
	# ==========================================
	def	load_data(self):
		try:
			with open("state.json", "r", encoding="utf-8") as f:
				data = json.load(f)
			# ==========================================
			# 데이터 정상 로드 시, 파일 -> 객체 변환 작업을 진행
			# 퀴즈 데이터 역직렬화 (deserialization)
			# ==========================================
			for item in data["quizzes"]:
				q = Quiz(item["question"],item["choices"], item["answer"])
				self.quizzes.append(q)
			#최고 점수 로드
			self.best_score = data["best_score"]
		except FileNotFoundError:
			print("파일이 존재하지 않습니다, 기본 퀴즈로 진행합니다.")
			self.quizzes = default_quiz
		except json.JSONDecodeError:
				print("파일 변환에 실패하였습니다, 기본 퀴즈로 진행합니다.")
				self.quizzes = default_quiz

	# ==========================================
	# 퀴즈 데이터 저장 메서드
	# ==========================================
	def	save_data(self):
		data = {
			"quizzes": [],
			"best_score": self.best_score
		}
		for q in self.quizzes:
			data["quizzes"].append({
				"question": q.question,
				"choices": q.choices,
				"answer": q.answer
			})
		with open("state.json", "w", encoding="utf-8") as f:
			json.dump(data, f, ensure_ascii=False, indent=4)

	def	show_menu(self):
		print('========================')
		print('나만의 퀴즈 게임')
		print('========================')
		print('1. 퀴즈 풀기')
		print('2. 퀴즈 추가')
		print('3. 퀴즈 목록')
		print('4. 점수 확인')
		print('5. 종료')
		print('========================')
	
	def play_quiz(self):
		# 퀴즈가 없는 경우의 처리 
		if len(self.quizzes) == 0:
			print('등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가 해 주세요.')
			return
		print(f'퀴즈를 시작합니다. 총 {len(self.quizzes)}문제')
		print('============================')
		#점수 초기화
		score = 0
		#문제 출력
		for i in range(len(self.quizzes)):
			if self.is_exit == True:
				break
			print(f'[문제 {i+1}]')
			print(f'{self.quizzes[i].question}')
			for j in range(len(self.quizzes[i].choices)):
				print(f'{j+1}. {self.quizzes[i].choices[j]}')
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
					if user_answer < 1 or user_answer > len(self.quizzes[i].choices):
						print('잘못된 입력입니다. 범위 내 선택지를 입력 하세요.')
						continue
					#정답 검증
					if self.quizzes[i].check_answer(user_answer):
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
					self.is_exit = True
					break
		#문제 풀이 후 스코어 및 정답 개수 처리
		if not self.is_exit:
			print(f'{len(self.quizzes)}문제 중 {score}문제 정답!')
			if self.best_score is None or score > self.best_score:
				print('새로운 최고 점수입니다.')
				self.best_score = score

	def	add_quiz(self):
		print('퀴즈를 추가합니다')
		while True:
			try:
				tmp_quiz = input('퀴즈 입력 : ').strip()
				if tmp_quiz == '':
					print('퀴즈를 입력 해 주세요.')
					continue
				result = []
				tmp_choices = input('선택지 입력 (,로 구분, 기본 4개) : ').split(',')
				for c in tmp_choices:
					result.append(c.strip())
				tmp_choices = result
				if len(tmp_choices) < 4:
					print('선택지는 최소 4개 이상 입력해 주세요.')
					continue
				tmp_raw = input('정답 입력 :').strip()
				tmp_answer = int(tmp_raw)
				if tmp_answer < 1 or tmp_answer > len(tmp_choices):
					print('선택지보다 큰 정답이 입력되었습니다')
					continue
			except ValueError:
				print('잘못된 정답이 입력되었습니다.')
				continue
			except (KeyboardInterrupt, EOFError):
					print('프로그램을 종료합니다. [Ctrl+C 또는 EOFError 발생]')
					self.is_exit = True
					break
			#객체 생성
			new_quiz = Quiz(tmp_quiz, tmp_choices, tmp_answer)
			#퀴즈 리스트 추가
			self.quizzes.append(new_quiz)
			print('퀴즈가 추가되었습니다.')
			break

	def	show_quiz_list(self):
		if len(self.quizzes) == 0:
			print('등록된 퀴즈가 없습니다.')
		else:
			print(f'등록된 퀴즈 목록 (총 {len(self.quizzes)}개)')
			for i in range(len(self.quizzes)):
				print(f' [{i+1}] {self.quizzes[i].question}')

	def	show_score(self):
		if self.best_score is None:
			print(f'아직 문제를 풀지 않았습니다.')
		else:
			print(f'최고 점수 : {self.best_score}점')

	def	run(self):
		while True:
			if self.is_exit == True:
				break
			self.show_menu()
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
				self.play_quiz()
			elif opt == 2:
				self.add_quiz()
			elif opt == 3:
				self.show_quiz_list()
			elif opt == 4:
				self.show_score()
			elif opt == 5:
				print('종료')
				break
			else:
				print('잘못된 입력입니다.')
				continue
		self.save_data()
		print('저장되었습니다.')

game = QuizGame()
game.run()
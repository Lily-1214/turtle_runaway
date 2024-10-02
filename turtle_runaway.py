import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2
        self.score = 0  # 점수 시스템 추가
        self.time_left = 60  # 60초 타이머 추가

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # 게임 시작 시 타이머를 실행
        self.start_time = time.time()
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        # 현재 시간을 기준으로 남은 시간 계산
        elapsed_time = time.time() - self.start_time
        self.time_left = max(60 - int(elapsed_time), 0)

        if self.time_left == 0:
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(-200, 300)
            self.drawer.write(f'Game Over! Final Score: {self.score}', font=("Arial", 16, "bold"))
            return  # 타이머가 0이 되면 게임 종료

        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        is_catched = self.is_catched()

        if is_catched:
            self.score = 0  # 잡히면 점수는 0으로 리셋
            self.drawer.undo()
            self.drawer.penup()
            self.drawer.setpos(-300, 300)
            self.drawer.write(f'Caught! Score: {self.score}', font=("Arial", 16, "bold"))
        else:
            self.score += 1  # 도망가는 시간에 비례해서 점수 증가

        # 점수 및 타이머 출력
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.drawer.write(f'Score: {self.score}, Time Left: {self.time_left}', font=("Arial", 16, "bold"))

        # 게임을 계속 진행
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass  # Manual control, no AI required

class IntelligentChaser(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, runner_pos, runner_heading):
        # chaser가 runner의 위치를 추적하는 간단한 AI
        self.setheading(self.towards(runner_pos))
        self.forward(self.step_move)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # User-controlled runner와 Intelligent AI chaser 설정
    runner = ManualMover(screen)
    chaser = IntelligentChaser(screen)

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()

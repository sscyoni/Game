from tkinter import *
import random
import time

tk = Tk()
tk.title("Game")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)

canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

score = 0
score_text = canvas.create_text(450, 20, text="Score: 0", font=("Helvetica", 14), fill="black")
game_over_text = None
restart_button = None


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)

        self.x = 0
        self.canvas_width = self.canvas.winfo_width()

        self.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        self.canvas.bind_all("<KeyPress-Right>", self.turn_right)

    def turn_left(self, evt):
        self.x = -3

    def turn_right(self, evt):
        self.x = 3

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)

        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle

        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.reset_position()

        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()
        self.hit_bottom = False

    def reset_position(self):
        self.canvas.coords(self.id, 10, 10, 25, 25)
        self.canvas.move(self.id, 245, 100)

        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)

        self.x = starts[0]
        self.y = -3

        self.hit_bottom = False

    def hit_paddle(self, pos):
        global score

        paddle_pos = self.canvas.coords(self.paddle.id)

        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                score += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3

        if pos[3] >= self.canvas_height:
            self.hit_bottom = True

        if not self.hit_bottom:
            if self.hit_paddle(pos):
                self.y = -3

        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3


paddle = Paddle(canvas, "blue")
ball = Ball(canvas, paddle, "red")


def reset_game():
    global score, game_over_text, restart_button

    score = 0
    canvas.itemconfig(score_text, text="Score: 0")

    ball.reset_position()

    if game_over_text:
        canvas.delete(game_over_text)
        game_over_text = None

    if restart_button:
        restart_button.destroy()

    game_loop()


def game_loop():
    global game_over_text, restart_button

    if not ball.hit_bottom:
        ball.draw()
        paddle.draw()
        tk.after(10, game_loop)
    else:
        game_over_text = canvas.create_text(250, 180, text="GAME OVER", font=("Helvetica", 30), fill="red")

        restart_button = Button(tk, text="Restart", font=("Helvetica", 14), command=reset_game)
        restart_button.pack(pady=20)


game_loop()
tk.mainloop()

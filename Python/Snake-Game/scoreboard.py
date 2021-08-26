from turtle import Turtle

ALIGNMENT = "center"
FONT = ("Courier", 15, "normal")


class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.setposition(x=0, y=275)
        with open("data.txt", "r") as file:
            self.highscore = int(file.read())
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.write(align=ALIGNMENT, arg=f"Score: {self.score}  High Score: {self.highscore}", font=FONT)

    def update_score(self):
        self.clear()
        self.score += 1
        self.update_scoreboard()

    def reset(self):
        if self.score > self.highscore:
            with open("data.txt", "w") as file:
                self.highscore = self.score
                file.write(f"{self.highscore}")
        self.score = 0
        self.update_scoreboard()

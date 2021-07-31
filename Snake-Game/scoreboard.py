from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier",15,"normal")

class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.setposition(x=0, y=275)
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(align=ALIGNMENT, arg=f"Score: {self.score}", font=FONT)

    def update_score(self):
        self.clear()
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0,0)
        self.write(align=ALIGNMENT,arg="GAME OVER",font=FONT)
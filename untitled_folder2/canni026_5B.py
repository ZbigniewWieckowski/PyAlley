from tkinter import *
from canni026_5A import RPSai 

win = Tk()
win.wm_title("Rock, Paper, Scissors")
win.geometry("400x400")

def winner(p1,p2):
    if p1+p2 in ["RS","SP","PR"]:
        return 1
    if p1==p2:
        return 0
    else:
        return -1

class UI:

    def __init__(self):
        self.rockB = Button(win, text="Rock", command =
self.rockPressed)
        self.paperB = Button(win, text="Paper", command =
self.paperPressed) #change the text
        self.scissorsB = Button(win, text="Scissors", command =
self.scissorsPressed) #change the text
        self.rockB.place(x=30,y=300)
        self.paperB.place(x=160,y=300)
        self.scissorsB.place(x=300,y=300)
        self.myAI = RPSai()
        self.wins = 0
        self.games = 0

        self.status = Label(win, text="Choose!",font=("Helvitica",40))
        self.status.place(x=20,y=150)

        self.winRate = Label(win, text="-",font=("Helvitica",30))
        self.winRate.place(x=20,y=50)

        self.gameCount = Label(win, text="-",font=("Helvitica",30))
        self.gameCount.place(x=320,y=50)

    def rockPressed(self):
        self.playRound("R")

    def paperPressed(self):
        self.playRound("P")

    def scissorsPressed(self):
        self.playRound("S")

    def playRound(self,move):
        cpuMove = self.myAI.playMovePro()
        self.myAI.opponentMove(move)

        #Code here to see who won
        # 1: Human won
        #-1: Human lost
        # 0: Human and AI tied

        if move == "R":
            if cpuMove == "P": 
                win = -1
            elif cpuMove == "S":
                win = 1
            else:
                win = 0
        elif move == "P":
            if cpuMove == "S": 
                win = -1
            elif cpuMove == "R":
                win = 1
            else:
                win = 0
        else:
            if cpuMove == "R": 
                win = -1
            elif cpuMove == "P":
                win = 1
            else:
                win = 0

        self.games += 1
        if win == 1:
            result = "Win"
            self.wins += 1
        elif win == -1:
            result = "Loose"
        else:
            result = "Tie"
            self.wins += .5

        self.gameCount["text"] = "%d"%(self.games) #updates game count
        self.status["text"] = "%s vs %s - You: %s"%(move,cpuMove,result)
        self.winRate["text"] = "%d"%(self.wins) #update the winrate

myUI = UI()
mainloop()

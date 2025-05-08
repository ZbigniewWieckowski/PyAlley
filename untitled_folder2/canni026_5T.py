import random

class RPSai:

    def __init__(self):
        self.R = 0
        self.P = 0
        self.S = 0
        self.history = []

    def opponentMove(self,m):
        if m == "R":
            self.R += 1
            self.history.append(m)
        elif m == "P":
            self.P += 1
            self.history.append(m)
        elif m == "S":
            self.S += 1
            self.history.append(m)
        else:
            return "Error."

    def beatMove(self,e):
        if e == "R":
            return "P"
        elif e == "P":
            return "S"
        elif e == "S":
            return "R"
        else:
            return "Error."

    def predictMove(self):
        mx = max(self.P,self.R,self.S)
        mxl = []
        if self.R == mx:
            mxl.append("R")
        if self.S == mx:
            mxl.append("S")
        if self.P == mx:
            mxl.append("P")
        ix = random.randint(1,len(mxl))
        return mxl[ix-1]
            

    def playMove(self):
        m = self.predictMove()
        if m == "R":
            return "P"
        if m == "P":
            return "S"
        else:
            return "R"

    def counterMove(self,om):
        if om == "R":
            return "P"
        if om == "P":
            return "S"
        else:
            return "R"
        

    def playMovePro(self):
        pat = True
        l2 = []
        l3 = []
        l4 = []
        l5 = []
        l6 = []
        l7 = []
        l8 = []
        l9 = []
        l10 = []
        if len(self.history) >= 30:
            for ix in range(15):
                l2.append(self.history[ix*2:ix*2+2])
            for i in l2:
                pat = i[0] == l2[0][0] and i[1] == l2[0][1]
                if not pat:
                    break
            if pat:
                return self.counterMove(l2[0][len(self.history)%2])
                    

        if len(self.history) >= 30:
            for ix in range(10):
                l3.append(self.history[ix*3:ix*3+3])
            for i in l3:
                pat = i[0] == l3[0][0] and i[1] == l3[0][1] and i[2] == l3[0][2]
                if not pat:
                    break
            print(pat)
            if pat:
                return self.counterMove(l3[0][len(self.history)%3])

        if len(self.history) >= 28:
            for ix in range(7):
                l4.append(self.history[ix*4:ix*4+4])
            for i in l4:
                pat = i[0] == l4[0][0] and i[1] == l4[0][1] and i[2] == l4[0][2] and i[3] == l4[0][3]
                if not pat:
                    break
            if pat:
                return self.counterMove(l4[0][len(self.history)%4])

        if len(self.history) >= 30:
            for ix in range(6):
                l5.append(self.history[ix*5:ix*5+5])
            for i in l5:
                pat = i[0] == l5[0][0] and i[1] == l5[0][1] and i[2] == l5[0][2] and i[3] == l5[0][3] and i[4] == l5[0][4]
                if not pat:
                    break
            if pat:
                return self.counterMove(l5[0][len(self.history)%5])

        if len(self.history) >= 30:
            for ix in range(5):
                l6.append(self.history[ix*6:ix*6+6])
            for i in l6:
                pat = i[0] == l6[0][0] and i[1] == l6[0][1] and i[2] == l6[0][2] and i[3] == l6[0][3] and i[4] == l6[0][4] and i[5] == l6[0][5]
                if not pat:
                    break
            if pat:
                return self.counterMove(l6[0][len(self.history)%6])

        if len(self.history) >= 28:
            for ix in range(4):
                l7.append(self.history[ix*7:ix*7+7])
            for i in l7:
                pat = i[0] == l7[0][0] and i[1] == l7[0][1] and i[2] == l7[0][2] and i[3] == l7[0][3] and i[4] == l7[0][4] and i[5] == l7[0][5] and i[6] == l7[0][6]
                if not pat:
                    break
            if pat:
                return self.counterMove(l7[0][len(self.history)%7])

        if len(self.history) >= 32:
            for ix in range(4):
                l8.append(self.history[ix*8:ix*8+8])
            for i in l8:
                pat = i[0] == l8[0][0] and i[1] == l8[0][1] and i[2] == l8[0][2] and i[3] == l8[0][3] and i[4] == l8[0][4] and i[5] == l8[0][5] and i[6] == l8[0][6] and i[7] == l8[0][7]
                if not pat:
                    break
            if pat:
                return self.counterMove(l8[0][len(self.history)%8])

        if len(self.history) >= 27:
            for ix in range(3):
                l9.append(self.history[ix*9:ix*9+9])
            for i in l9:
                pat = i[0] == l9[0][0] and i[1] == l9[0][1] and i[2] == l9[0][2] and i[3] == l9[0][3] and i[4] == l9[0][4] and i[5] == l9[0][5] and i[6] == l9[0][6] and i[7] == l9[0][7] and i[8] == l9[0][8]
                if not pat:
                    break
            if pat:
                return self.counterMove(l9[0][len(self.history)%9])

        if len(self.history) >= 30:
            for ix in range(3):
                l10.append(self.history[ix*10:ix*10+10])
            for i in l10:
                pat = i[0] == l10[0][0] and i[1] == l10[0][1] and i[2] == l10[0][2] and i[3] == l10[0][3] and i[4] == l10[0][4] and i[5] == l10[0][5] and i[6] == l10[0][6] and i[7] == l10[0][7] and i[8] == l10[0][8] and i[9] == l10[0][9]
                if not pat:
                    break
            if pat:
                return self.counterMove(l10[0][len(self.history)%10])
        
        a = self.playMove()
        return a
        

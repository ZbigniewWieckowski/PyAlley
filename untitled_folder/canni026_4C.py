import math

class Money:
    def __init__(self,dollars,cents=0):
        self.dollars = dollars + cents//100
        self.cents = cents%100
        if self.dollars < 0 and self.cents != 0:    
            self.dollars += 1
            self.cents -= 100
        

    def __repr__(self):
        if abs(self.cents) < 10:
            return "$" + str(self.dollars) + ".0" + str(abs(self.cents))
        else:
            return "$" + str(self.dollars) + "." + str(abs(self.cents))

    def __add__(self,r):
        return Money(self.dollars + r.dollars, self.cents + r.cents)
        
    def __sub__(self,r):
        return Money(self.dollars - r.dollars, self.cents - r.cents)

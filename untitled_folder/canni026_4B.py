class Ant:
    def __init__(self,ls=10):
        self.linesize = ls
        self.pos = 0 
        self.dir = 1

    def step(self):
        tst = self.pos + self.dir
        if tst < 0 or tst > self.linesize - 1:
            return "error"
        else:
            self.pos = tst

    def turn(self):
        self.dir = -self.dir

    def setPos(self,x):
        if x < 0 or x > 10:
            return "error"
        else:
            self.pos = x

    def display(self):
        print("'"+ "." * self.pos + (self.dir+1)//2*'>'+(1-self.dir)//2*'<'+(self.linesize - self.pos - 1)*"."+"'")
        
            

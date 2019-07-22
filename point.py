class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init
        self.angulo=0

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ") ->",str(self.angulo)])

    def __lt__(self,p):
        if self.x<p.x:
            retorno =self
        else:
            if self.x == p.x:
                if self.y<p.x:
                    retorno= self
                else:
                    retorno = p
            else:
                retorno = p
        return retorno
    def angulo (p):
        return p.angulo

from tupy import *

# TODO: implementação em andamento, com bugs

class Arvore(TupyObject):
    def __init__(self, valor_da_raiz):
        self.raiz = No(valor_da_raiz)
        self.raiz._posiciona(400, 10)
    
    @property
    def x(self):
        return self.raiz.x
    @property
    def y(self):
        return self.raiz.y
    @property
    def _width(self):
        return self.raiz._width
    @property
    def _height(self):
        return self.raiz._height


class No(TupyObject):
    def __init__(self, valor, nivel=1, parent=None):
        self.esquerda = None
        self.direita = None
        self.valor = valor
        self.label = Label(valor, 0, 0)
        self.nivel = nivel
        self.parent = parent

    def _posiciona(self, x, y):
        self.label.x = x
        self.label.y = y

    def adiciona_esquerda(self, valor):
        if self.esquerda is not None:
            self.esquerda.destroy()
        self.esquerda = No(valor, self.nivel + 1, self)
        self.esquerda._posiciona(self.label.x - 100 / self.nivel, self.label.y + 100)
    
    def adiciona_direita(self, valor):
        self.direita = No(valor, self.nivel + 1, self)
        self.direita._posiciona(self.label.x + 100 / self.nivel, self.label.y + 100)

    def __repr__(self) -> str:
        return f' {self.valor}'

    @property
    def x(self):
        return self.label.x
    @property
    def y(self):
        return self.label.y
    @property
    def _width(self):
        return self.label._width
    @property
    def _height(self):
        return self.label._height

    def destroy(self):
        self.label.destroy()
        if self.esquerda is not None:
            self.esquerda.destroy()
        if self.direita is not None:
            self.direita.destroy()
        if self.parent is not None:
            if self == self.parent.esquerda:
                self.parent.esquerda = None
            elif self == self.parent.direita:
                self.parent.direita = None
        super().destroy()

arvore = Arvore('raiz')
arvore.raiz.adiciona_esquerda('a')
arvore.raiz.adiciona_direita('b')

run(globals())
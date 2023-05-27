# Grupos de objetos

`BaseGroup` e `Group` são classes de conveniência que permitem agrupar objetos do Tupy em um único objeto. Por exemplo, se você quiser mover um grupo de objetos, basta mover o grupo que os contém. A classe `BaseGroup` possui membros privados e foi feita para ser estendida por outras classes, enquanto a classe `Group` funciona da mesma forma, mas com membros públicos.

## BaseGroup

Além dos atributos e métodos herdados de `BaseTupyObject`, `BaseGroup` define os seguintes atributos e métodos:

- `_objects`: lista com todos os objetos contidos no `BaseGroup`. Essa lista não deve ser alterada diretamente, e sim através dos métodos `_add`, `_remove` e `_clear`.
- `_add(obj)`: adiciona um objeto à lista de objetos contidos no `BaseGroup`.
- `_remove(obj)`: remove um objeto da lista de objetos contidos no `BaseGroup`.
- `_clear()`: remove todos os objetos da lista de objetos contidos no `BaseGroup`.

Exemplo de uso de `BaseGroup`:

```python
from tupy import *

class Constelacao(BaseGroup):
    def __init__(self):
        super().__init__(x, y)
        self._add(Image('estrela.png', 100, 100))
        self._add(Image('estrela.png', 150, 150))
    
    def update(self):
        self._x += 1
        self._y += 1

cons = Constelacao()

run(globals())
```

## Group

`Group` possui os mesmos atributos e métodos, porém públicos. Além disso, `Group` possui `x` e `y` públicos.

O construtor de `Group` recebe, opcionalmente, uma lista de objetos que serão adicionados ao grupo. Por exemplo:

```python
from tupy import *

grupo = Group([
  Image('star.png', 100, 100),
  Image('star.png', 150, 150)
])

def update():
  grupo.x += 1

run(globals())
```
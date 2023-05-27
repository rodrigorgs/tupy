# Atualização de tela

O Tupy atualiza a tela cerca de 30 vezes por segundo e, com isso, é capaz de exibir animações. Para isso, é necessário alterar o estado dos objetos da cena ao longo do tempo. Para isso, você pode implementar uma função `update()` ou, ainda, implementar um método `update()` nas classes dos objetos que devem ser alterados.

## Função update

A função `update()` é chamada a cada quadro da animação. Por exemplo:

```python
from tupy import *

estrela1 = Image('star.png')
estrela2 = Image('star.png')

def update():
  estrela1.angle += 5

run(globals())
```

Nesse exemplo, a função `update()` é chamada a cada quadro da animação. A cada quadro, o ângulo da primeira estrela é incrementado em 5 graus. Isso faz com que a estrela gire continuamente.

## Método update

Outra forma de atualizar o estado dos objetos é implementar um método `update()` nas classes dos objetos que devem ser alterados. Por exemplo:

```python
from tupy import *

class Star(Image):
  def update(self):
    self.angle += 5

estrela1 = Star('star.png')
estrela2 = Star('star.png')

run(globals())
```

Nesse caso, não é necessário definir uma função `update()` além do método `update()` da classe `Star`. A cada quadro, o método `update()` de cada estrela é chamado. Isso faz com que ambas as estrelas girem continuamente.

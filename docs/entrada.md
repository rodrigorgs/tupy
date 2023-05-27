# Teclado e mouse

Programas escritos para o Tupy podem responder a eventos de teclado e mouse. Para isso, é necessário chamar métodos específicos dentro da função `update()` ou do método `update()` de uma classe.

## Teclado

O Tupy define uma variável global `keyboard`, com três métodos:

- `keyboard.is_key_down(key)`: retorna `True` se a tecla `key` está pressionada, ou `False` caso contrário
- `keyboard.is_key_up(key)`: retorna `True` se a tecla `key` não está pressionada, ou `False` caso contrário
- `keyboard.is_key_just_down(key)`: retorna `True` se a tecla `key` acabou de ser pressionada neste instante, ou `False` caso contrário

O parâmetro `key` é uma string que representa uma tecla do teclado. Por exemplo, `'left'` representa a tecla de seta para a esquerda, `'a'` representa a tecla `a`, `'space'` representa a barra de espaço, etc. A lista completa de strings pode ser encontrada no [manual do Tk](https://www.tcl.tk/man/tcl8.4/TkCmd/keysyms.html)

Exemplo de uso:

```python
from tupy import *

class Star(Image):
  def update(self):
    if keyboard.is_key_down('left'):
      self.x -= 2
    if keyboard.is_key_down('right'):
      self.x += 2
    if keyboard.is_key_just_down('space'):
      # volta para posição inicial
      self.x = 20
      self.y = 20

estrela = Star('star.png')
estrela.x = 20
estrela.y = 20

run(globals())
```

## Mouse

O Tupy define uma variável global `mouse`, com os seguintes membros:

- atributos `x` e `y`: definem a posição do ponteiro do mouse, relativamente à área de visualização da cena
- método `is_button_down()`: retorna `True` se o botão do mouse está pressionado, ou `False` caso contrário
- método `is_button_just_down()`: retorna `True` se o botão do mouse acabou de ser pressionado neste instante, ou `False` caso contrário

Exemplo de uso:

```python
from tupy import *

class Star(Image):
  def update(self):
    self.x = mouse.x
    self.y = mouse.y

    if mouse.is_button_just_down():
      self.angle += 30

s = Star()

run(globals())
```
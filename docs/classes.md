# Outros tipos de objetos

O Tupy permite criar outros tipos de objetos além de imagens. Por exemplo, é possível criar retângulos, círculos, ovais e textos.

## Retângulo

Para criar um Retângulo:

```python
Rectangle(x, y, width, height, outline = 'black', fill = ''):
```

Onde:

- `x, y` é a posição do canto superior esquerdo do retângulo
- `width, height` é o tamanho do retângulo (largura e altura)
- `outline` é a cor da borda do retângulo (por padrão, preta)
- `fill` é a cor do preenchimento do retângulo (por padrão, transparente)

Os atributos `outline` e `fill` são cores, que podem ser representadas da seguinte forma:

- `''` (string vazia): transparente
- `#RGB` ou `#RRGGBB`: cor em RGB, onde R, G e B são números hexadecimais de 0 a F
- Um dos [nomes de cores reconhecidos pelo Tk](https://www.tcl.tk/man/tcl/TkCmd/colors.html)

Exemplo de uso:

```python
from tupy import *

r = Retangulo(10, 10, 100, 50, outline = 'red', fill = 'yellow')

run(globals())
```

## Círculo e oval

Para criar um oval ou um círculo:

```python
Oval(x, y, width, height, outline = 'black', fill = ''):
```

Os parâmetros são os mesmos da classe `Rectangle` (ver acima).

## Texto

Para criar um texto:

```python
Label(x, y, text, font = 'Arial 20', color = 'black', anchor = 'nw'):
```

Onde:

- `x, y` é a posição do texto (ver o parâmetro `anchor` abaixo)
- `text` é o texto a ser exibido (string)
- `font` é a fonte do texto (por padrão, Arial tamanho 20)
- `color` é a cor do texto (por padrão, preta)
- `anchor` é o ponto de referência do texto. Pode ser um dos seguintes valores:
  - `'nw'`: canto superior esquerdo
  - `'n'`: centro superior
  - `'ne'`: canto superior direito
  - `'w'`: centro esquerdo
  - `'center'`: centro
  - `'e'`: centro direito
  - `'sw'`: canto inferior esquerdo
  - `'s'`: centro inferior
  - `'se'`: canto inferior direito

Exemplo de uso:

```python
from tupy import *

t = Label(10, 10, 'Olá mundo!')

run(globals())
```

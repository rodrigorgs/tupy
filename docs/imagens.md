# Imagens

O tipo `Image` é um dos mais comuns em programas escritos para o Tupy. Ele representa uma imagem que pode ser exibida na tela. A classe `Image` possui os seguintes atributos:

- `x` e `y`: coordenadas da imagem na tela
- `file`: nome do arquivo de imagem, no formato PNG
- `angle`: ângulo de rotação da imagem, em graus

O Tupy busca o arquivo de imagem nos seguintes locais, em ordem:

- no diretório onde se encontra o script
- no subdiretório `assets` do diretório onde se encontra o script
- no diretório de instalação do pacote Tupy

O Tupy já vem com algumas imagens de exemplo, que podem ser usadas diretamente pelo nome: `star.png`, `star2.png`, `ball.png`, `smiley.png`, `drone.png`.

## Criando uma imagem

Para criar uma imagem, basta instanciar a classe `Image`:

```python
Image(file, x, y)
```

Os parâmetros `x` e `y` são opcionais; se omitidos, a imagem é criada em uma posição aleatória.

Exemplo de código:

```python
from tupy import *

a = Image('star.png', 100, 200)
b = Image('star2.png') # posição aleatória
b.angle = 30

run(globals())
```

## Criando sua própria classe

Outra forma de criar imagens é criando uma classe estende a classe `Image`. Por exemplo:

```python
from tupy import *

class Star(Image):
  def __init__(self):
    self.angle = 30

a = Star()
a.x = 100
a.y = 200

run(globals())
```

No exemplo, a classe `Star` herda os atributos e métodos de `Image`, como `x`, `y`, `file` e `angle`. A classe `Star` não adiciona nenhum atributo ou método novo, mas poderia fazê-lo.

Ao ser inicializada, a estrela é rotacionada em 30 graus. Além disso, a estrela é criada em uma posição aleatória, e em seguida a posição é alterada para (100, 200).

Note que, no exemplo, não foi definido o nome do arquivo de imagem. Nesse caso, o Tupy procura um arquivo com o mesmo nome da classe (em minúsculas), seguido de `.png`. Ou seja, nesse exemplo o nome do arquivo é `star.png`. Se necessário, é possível alterar o nome do arquivo, atribuindo um novo valor ao atributo `file`.

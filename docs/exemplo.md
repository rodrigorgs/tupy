# Primeiro exemplo

Crie um script Python com o seguinte conteúdo:

```python
from tupy import *

class Star(Image):
	def update(self):
		self.y += 2

star1 = Star()
star2 = Star()
star1.x = 100
star2.x = 200

run(globals())
```

## Explicação

A primeira linha importa o módulo `tupy`, que contém as classes e funções necessárias para criar programas interativos.

As três linhas seguintes definem uma classe `Star` que herda da classe `Image`. A classe `Image` representa uma imagem que pode ser exibida na tela. A classe `Star` adiciona um método `update` que é chamado a cada quadro da animação. Esse método faz com que a estrela caia 2 pixels a cada quadro.

As quatro linhas seguintes criam duas instâncias da classe `Star` e as posicionam na tela.

Por fim, a última linha abre a janela do Tupy e inicia a animação.

## Executando

Por fim, execute o script com o interpretador Python. Isso deve abrir o Tupy e mostrar duas estrelas caindo.

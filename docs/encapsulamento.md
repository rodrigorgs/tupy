# Encapsulamento

A classe `Image` possui atributos públicos, como `x` e `y`. Isso permite que o usuário altere a posição da imagem diretamente pela interface do Tupy ou então através de código.

Isso pode ser um problema quando criamos uma subclasse de `Image`, como `Carro`. É desejável que o carro se mova apenas para frente e para trás, mas não para os lados. Para isso criamos métodos como `avanca` e `recua`, que alteram a posição do carro.

O problema é que, mesmo com esses métodos, o usuário ainda consegue alterar a posição do carro diretamente, fazendo-o andar para os lados ou teleportar-se para qualquer lugar da tela.

Em Python, podemos esconder um membro de uma classe (atributo ou método) dando-lhe um nome iniciado por `_`. Com isso o membro deixa de ficar visível no ambiente do Tupy, obrigando o usuário a usar os métodos da classe para alterar a posição do carro. Membros cujo nome se inicia por `_` são chamados de **privados**.

(Observação: o usuário até pode acessar membros privados se usar o console do Tupy, então o uso de membros privados é mais uma recomendação para não acessar do que uma forma de segurança.)

## Classe BaseImage

A classe `BaseImage` é muito parecida com a classe `Image`, exceto que todos os seus atributos são privados: `_x`, `_y`, `_file` e `_angle`.  Não se deve instanciar objetos dessa classe diretamente, mas sim através de suas subclasses. As subclasses podem acessar os atributos privados da classe `BaseImage` através de métodos.

Exemplo:

```python
from tupy import *

class Carro(BaseImage):
  def __init__(self):
    super().__init__('carro.png', 100, 100)
    
  def avanca(self):
    self._x += 10

  def recua(self):
    self._x -= 10
```

No exemplo, os atributos não aparecem no ambiente Tupy, o que indica que o usuário não deve alterá-los diretamente. Apenas a posição no eixo X pode ser alterada, e ainda assim, de forma controlada, de 10 em 10 pixels, através dos métodos `avanca` e `recua`.


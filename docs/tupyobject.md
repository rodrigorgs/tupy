# BaseTupyObject

`BaseTupyObject` é a classe base de todos os objetos do Tupy, que são os objetos que aparecem na cena. Ela define os atributos e métodos comuns a todos os objetos do Tupy.

Algumas subclasses de `BaseTupyObject` são `BaseImage`, `Image`, `Rectangle`, `Oval` e `Label`. As subclasses podem definir atributos e métodos adicionais, mas todas elas herdam os atributos e métodos de `BaseTupyObject`.

## Atributos

- `_x`, `_y`: posição do objeto na cena. Cada subclasse define o ponto de referência usado para posicionar o objeto. Por exemplo, na classe `Rectangle`, o ponto de referência é o canto superior esquerdo do retângulo. Na classe `Image`, o ponto de referência é o centro da imagem.
- `_width`, `_height`: largura e altura do objeto. Se o objeto não for retangular, ainda assim ele deve definir a largura e a altura de um retângulo que o contém.

## Métodos

- `_hide()`, `_show()`: esconde e mostra o objeto na cena.
- `_contains_point(x, y)`: método de conveniência que indica se o ponto (x, y) está dentro do retângulo formado por `_x`, `_y`, `_width`, `_height`.
- `_collides_with(outro)`: método de conveniência que indica se o objeto colide com outro objeto. O objeto passado como parâmetro deve ser uma instância de `BaseTupyObject` ou de uma de suas subclasses.
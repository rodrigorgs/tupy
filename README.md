# Tupy

Tupy is a graphical environment in which people can experiment with Python objects. It is inspired by Java's Greenfoot.

## Installing

To install Tupy, run the following command:

```sh
pip install git+https://github.com/rodrigorgs/tupy.git
```

## Using

Here's a simple program that uses Tupy:

```python
import tupy

class Star(tupy.Object):
	def update(self):
		self.x += 5
		self.y += 5

star1 = Star()
star2 = Star()
star1.x = 30
star2.x = 80

tupy.run(globals())
```

You will also need an image file named `star.png` in the same folder as your source code.

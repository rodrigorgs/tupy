# Tupy

Tupy is a graphical environment in which people can experiment with Python objects. It is inspired by Java's Greenfoot.

## Installing

To install the latest version of Tupy, run the following command:

```sh
pip install git+https://github.com/rodrigorgs/tupy.git
```

## Using

Here's a simple program that uses Tupy:

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

Save the file as a Python script and run it. For instance, if the file name is `example.py`, run it like this:

```sh
python example.py
```

All instances of the `Star` class will be displayed as the `star.png` image provided by Tupy; to customize the image, create a `star.png` image in the same folder as your script.

## Hot reload

Hot reload allows you to change your code while it's running and see the results without restarting your script. You can achieve hot reload with the Jurigged package.

To install Jurigged:

```sh
pip install jurigged
```

To run the `example.py` using hot reload:

```sh
jurigged example.py
```

# Gate To Gods

### Getting started

To start the game, Python 3 needs to be installed. 
On Windows, a console that support ANSI escape codes like [Aniscon](https://github.com/adoxa/ansicon) is recommended.
You can also use cmd if you activate the colours in the console itself.
Linux consoles supports ANSI escape codes by default.

Select the file "main.py" and start it with a parameter, which is the map that will first be opened by the game.

Additionally, it is possible to use additional parameters. Gate To Gods uses a Random Number Generator (RNG) that uses a seed.
If you add `-seed` or `-s` behind the map, you can set the seed the RNG will use.
The seed must be a number.
The same seed will always lead to the same results (i.e. enemy damage).
Not specifying a seed will use the system time instead.

The parameter `-log` or `-l` will record everything shown on screen. 
After the parameter you need to specify a file in which the game will be recorded.

Finally, the parameter `-view` or `-v` will replay a recorded file.
Again, the file which should be replayed needs to be the following parameter.

### Controls

- Move left: a or 4
- Move up: w or 8
- Move right: d or 6
- Move down: s or 2
- Move up-left: 7
- Move up-right: 9
- Move down-left: 1
- Move down-right: 3
- Open a door: o (or walk against it)
- Close a door: c
- Enter new map: < or >
- Next slide: n
- Previous slide: p
- Exit game: x


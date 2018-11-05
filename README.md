# SukiGD
A dialogue system that uses a simple scripting language based on RenPy, but built for Godot

Things that currently work:

  1. Transpiling from SukiGD to JSON

  2. Compile-Time error messages
  
Things that are being worked on:

  1. Parsing from JSON into Godot
  
  1a. Creating an optional run-time transpiler in GDScript so SukiGD files can be used directly instead
  
  2. The display system
  
HOW IT WORKS:

Step 1: Create a constants.txt file similar to the example in the input folder. This should contain declarations for all of your positions and characters. This is kept in a separate file so that you can load it automatically when the dialogue system is initialized in Godot. The following are the rules for constant declaration:
```
POSITIONS: //This is called a header. It is a special keyword that declares the beginning of your position declarations.

Position left = (0.2,0.5) //This is the constructor for Positions. Do not put spaces within the parentheses! The floating point values represent your position on the screen, with (0.0,0.0) being the top-left corner, and (1.0,1.0) being the bottom-right corner.

CHARACTERS: //The Characters header declares the beginning of character declarations

Character paul = "Paul" //The constructor for a Character object gives it a reference value and a PATH to its controller Node in Godot. "Paul" could be replaced with "res://assets/scenes/Paul.tscn" or something if you do your own implementation

Emotion happy
Emotion sad //The Emotion keyword is basically an enum in dictionary form. Characters["paul"]["happy"] will return 0, and Characters["paul"]["sad"] will return 1.
```

Step 2: Write your scripts. Each section of dialogue should be its own script to minimize load time. There are five legal statements in SukiGD scripts so far:
```
show [Character] [Emotion] at [Position] //Character, Emotion, and Position should all be constants declared in your constants file!

show [Character] [Emotion] [Position] //A 3-character less verbose version of the previous statement, for the lazy

hide [Character]

[Character] [Emotion] "String of dialogue" //This updates the Character's image and displays the dialogue

[Character] "String of dialogue" //This dislpays the dialogue without updating the Character's image
```
Step 3: Place all of your .txt files in the "input" folder and run SukiGD.py. Obviously, this requires Python.

Step 4: Check the output folder for your JSON files!
  
State of the Software:

While the transpiler currently works as intended if your syntax is correct, it does not have any form of error handling. This means that if your SukiGD code has a legal amount of arguments, it will transpile even if the syntax is incorrect. Because of the way the scanner and parser work, it is unlikely to not crash upon incorrect syntax, but it is possible to transpile incorrectly without errors.

A dialogue system in Godot has not been built yet, but please keep in mind that SukiGD is just a JSON parser. If you'd like, you are more than welcome to create a dialogue system that uses my JSON formatting.

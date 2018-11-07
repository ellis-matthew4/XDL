# SukiGD
A dialogue system that uses a simple scripting language based on RenPy, but built for Godot

Things that currently work:

  1. Transpiling from SukiGD to JSON

  2. Compile-Time error messages
  
  3. Parsing from JSON into Godot
  
  4. The display system
  
Things that might be worked on:
  
  1. Creating an optional run-time transpiler in GDScript so SukiGD files can be used directly instead
  
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

Step 5: Add the Display.tscn file to your Godot library and edit the scene to make it look the way you want it to

Step 6: Add your characters as children of the "Characters" node as AnimatedSprites or Sprites with TextureAtlases. Make sure that the frame order matches the enumeration of your emotions in your constants file. (Make sure they are in the same order)

Step 7: Create an instance of Display.tscn. The methods to use it are as follows:
```
loadConstants(filename) # use this to load constants. You can call this more than once, but keep in mind that calling it again will clear the current constants
read(filename) # triggers a dialogue sequence. By default, this does not pause the game.
```
  
State of the Software:

Scripts can be transpiled from SukiGD to JSON and read into Godot. The display system mostly works, I just need to have it actually load the text into the display. Iteration through statements is working as intended, and the enumerated display also works properly. The transpiler really doesn't like Windows's end line character, so I highly recommend using a tool such as dos2unix on your scripts before running them through. Cygwin can run python and dos2unix, so I reccomend using that if you're not scared of the command line.

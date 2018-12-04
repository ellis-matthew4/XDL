# SukiGD
A dialogue system that uses a simple scripting language based on RenPy, but compiles to a JSON format built for Godot

NOTE: The JSON format can theoretically be used by any engine, but for now the only one I am officially writing an interpreter for is Godot.

Things that currently work:

  1. Transpiling from SukiGD to JSON

  2. Compile-Time error messages
  
  3. Parsing from JSON into Godot
  
  4. The display system
  
Upcoming features:
  
  1. Animation handlers and a "with" keyword for use with "Scene", "Show", and "Hide" statements
  
Things that might be worked on:
  
  1. Creating an optional run-time transpiler in GDScript so SukiGD files can be used directly instead
  
HOW IT WORKS (Video soon(TM)):

Step 1: Create a constants.txt file similar to the example in the input folder. This should contain declarations for all of your positions and characters. This is kept in a separate file so that you can load it automatically when the dialogue system is initialized in Godot. You can find details on the syntax in the Wiki.

Step 2: Write your scripts. Each section of dialogue should be its own script to minimize load time. The syntax used in SukiGD can be found in the Wiki.

Step 3: Place all of your .txt files in the "input" folder and run SukiGD.py. Obviously, this requires Python.

Step 4: Check the output folder for your JSON files!

Step 5: Add the Display.tscn file to your Godot library and edit the scene to make it look the way you want it to. You will also want to edit display.gd in order to add transitions or any other effects. I recommend importing the entire SukiGD folder, but this is not absolutely necessary if you don't want to.

Step 6: Add your characters as children of the "Characters" node as AnimatedSprites. Make sure that the frame order matches the enumeration of your emotions in your constants file. (Make sure they are in the same order). Also add your backdrops as children of the Scenes Node2D. They should be Sprite nodes.

Step 7: Create an instance of Display.tscn. The methods to use it are as follows:
```
loadConstants(filename) # use this to load constants. You can call this more than once, but keep in mind that calling it again will clear the current constants
read(filename) # triggers a dialogue sequence. By default, this does not pause the game.
```
  
State of the Software:

Scripts can be transpiled from SukiGD to JSON and read into Godot. The display system works as intended. The transpiler really doesn't like Windows's end line character, so I highly recommend using a tool such as dos2unix on your scripts before running them through. Cygwin can run python and dos2unix, so I reccomend using that if you're not scared of the command line.

# XDL- Extensible Dialogue Language (Formerly SukiGD)
A label-oriented dialogue system that uses a simple scripting language based on RenPy, but compiles to a JSON format built for Godot

NOTE: The JSON format can theoretically be used by any engine, but for now the only one I am officially writing an interpreter for is Godot.

# IMPORTANT USAGE INFORMATION:
XDL uses a 0.5 second Timer to prevent it from reactivating itself at the end of a dialogue. If you use a yield(XDL, "done") statement in Godot, you need to make sure that that statement is also on a cooldown timer! If you do not do this, XDL will crash.

# Why should you use XDL?
It depends on your use case. You should use XDL if you meet the following criteria:
1) You want an easy-to-write language for your game's dialogue
2) Your game is not dialogue-only (Most Visual Novels fall under this category)

XDL is meant for games where the dialogue is just a layer on top of the actual gameplay, it is not meant to build visual novels. There are better tools for that kind of thing. Not to say that you can't, of course, just that it's not meant to be used that way.
  
# HOW IT WORKS (Video soon(TM)):

Step 1: Create a constants.txt file similar to the example in the input folder. This should contain declarations for all of your positions, backdrops, and characters. This is kept in a separate file so that you can load it automatically when the dialogue system is initialized in Godot. You can find details on the syntax in the Wiki.

Step 2: Write your scripts. Each section of dialogue should be its own script to minimize load time. The syntax used in XDL can be found in the Wiki.

Step 3: Place all of your .txt files in the "input" folder and run XDL.py. Obviously, this requires Python.

Step 4: Check the output folder for your JSON files!

Step 5: Add XDL's Godot Files folder and your scripts to your Godot library and edit the scene to make it look the way you want it to. I do not recommend editing any of XDL's scripts in order to add transitions or any other effects, these should be done in a wrapper function so that XDL functions normally. You also need to change some of the variables in Display.gd to match your file system.

Step 6: Add your characters as children of the "Characters" node as AnimatedSprites. Make sure that the frame order matches the enumeration of your emotions in your constants file. (Make sure they are in the same order). Also add your backdrops as children of the Scenes Node2D. They should be Sprite nodes.

Step 7: Create an instance of Display.tscn. The methods to use it are as follows:
```
loadConstants(filename) # use this to load constants. You can call this more than once, but keep in mind that calling it again will clear the current constants
read(filename) # reads a script file into memory
call(label) # calls a label from the currently loaded script file
jump(label) # clears the current context, then calls the given label (essentially GOTO)
get(variable) # returns a local variable from the currently loaded script file
```

# SFAQ (Somewhat Frequently Asked Questions)
> What do you mean by "label-oriented?"

Label-orientation refers to how the data is structured into named lists called labels. In future versions, rather than using RenPy's iterative approach to conditions and menus, XDL will use label referencing to handle flow control. This will increase the total number of labels, but it will allow for cleaner serialization that will take up significantly less space.

> Why can't I embed code into dialogue files like in RenPy?

The shortest reason is because XDL is meant to be compatible with any game engine. Allowing the user to code in GDScript would make a Unity interpreter fail. A longer answer would be because the goal is to decouple the dialogue from the game, and have the two send each other instructions rather than have XDL handle computations. The exception to this is flow control, as if statements will be able to perform very basic arithmetic.

> Will (Some feature) be implemented?
  
The short and possibly incorrect answer is no. The interpreter is designed to be extensible, so if you want a feature for your game, use the action keyword and implement it. You aren't meant to use the interpreter the exact way it comes out of the box, I fully expect you to edit it for your game.

# State of the Software:

Scripts can be transpiled from XDL to JSON and read into Godot. The display system works as intended. The transpiler really doesn't like Windows's end line character, so I highly recommend using a tool such as dos2unix on your scripts before running them through. Cygwin can run python and dos2unix, so I reccomend using that if you're not scared of the command line.

Several planned features, such as novel mode and encryption have been scrapped to keep the software as simple as possible. If your game uses novel mode, like Tsukihime or Fate/Stay Night, you'll want to rebuild the interpreter yourself to make sure it works the way you want it to. If I get enough requests, I will create a modified interpreter in another branch that handles novel mode.

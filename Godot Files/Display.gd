extends CanvasLayer

onready var projectRes = Vector2(ProjectSettings.get_setting("display/window/size/width"), ProjectSettings.get_setting("display/window/size/height"))
onready var charNodes = get_node("Characters")
onready var textBox = get_node("TextBox/TextControl/Dialogue")
onready var nameBox = get_node("TextBox/TextControl/Name")

var constants
var positions = {}
var characters = {}
var backdrops = {}
var dialogue = []
var current = 0
var active = false
var click = false
var wait = true

func _ready():
	loadConstants("constants.json") #Only run this command when necessary!
	set_process(true)
	
func _process(delta):
	if active: #Triggers upon a read() call
		# get_tree().call_group("playable_characters", "hideGUI") #My games' command to hide the HUD
		get_tree().paused = true #Remove this to disable pausing upon dialogue load
		get_node("TextBox").visible = true
		if Input.is_action_just_pressed("ui_select"):
			if current < len(dialogue):
				var statement = dialogue[current]
				if statement["action"] == "show":
					Show(statement)
					wait = true
				elif statement["action"] == "hide":
					Hide(statement)
					wait = true
				elif statement["action"] == "dialogue":
					dialogue(statement)
				elif statement["action"] == "scene":
					Scene(statement)
				current += 1
			else: # Reset and prepare for the next dialogue
				hideAll()
				current = 0
				active = false
				wait = true
		else:
			if wait: #This block of code prevents having to click for show and hide statements.
				if current < len(dialogue):
					var statement = dialogue[current]
					if statement["action"] == "show":
						Show(statement)
						current += 1
					elif statement["action"] == "hide":
						Hide(statement)
						current += 1
					elif statement["action"] == "dialogue":
						dialogue(statement)
						current += 1
						wait = false
	else:
		# get_tree().call_group("playable_characters", "showGUI") #My games' command to show the HUD
		get_tree().paused = false
	
func loadConstants(filename): # Load the constants to dictionaries for easy access
	var file = File.new()
	file.open("res://SukiGD/dialogue/" + filename, File.READ)
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO LOAD FILE " + filename)
		return
	constants = data.result
	for p in constants["Positions"]: #Create actual game positions that can be used
		var pos = Vector2()
		pos.x = float(constants["Positions"][p]["x"])
		pos.y = float(constants["Positions"][p]["y"])
		positions[p] = pos * projectRes
	var temp = constants["Characters"] #Create references to Character nodes
	for c in temp:
		characters[c] = temp[c]
		characters[c]["path"] = characters[c]["path"].replace('"',"")
	if constants.has("Backdrops"): #Create references to Scene nodes
		backdrops = constants["Backdrops"]
		for b in backdrops:
			backdrops[b] = backdrops[b].replace('"',"")
	
func read(filename):
	var file = File.new()
	file.open("res://SukiGD/dialogue/" + filename, File.READ) #Default filepath, you probably want to change this
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO READ FILE " + filename)
		return
	dialogue = data.result["dialogue"]
	active = true #Activate the dialogue loop
			
func Show(s): # Show statement
	var c = charNodes.get_node(characters[s["char"]]["path"])
	c.global_position = positions[s["pos"]]
	c.frame = characters[s["char"]][s["emote"]]
	c.visible = true
	
func Hide(s): # Hide statement
	var c = charNodes.get_node(characters[s["char"]]["path"])
	c.global_position = Vector2(0,0)
	c.visible = false
func hideAll(): # Hides SukiGD
	get_node("TextBox").visible = false
	get_node("TextBox/TextControl/Dialogue").text = ""
	get_node("TextBox/TextControl/Name").text = ""
	for c in charNodes.get_children():
		c.global_position = Vector2(0,0)
		c.visible = false
	for sc in $Scenes.get_children():
		sc.visible = false
		
func dialogue(s): # Displays a line of dialogue
	if s.has("emote"):
		var c = charNodes.get_node(characters[s["char"]]["path"])
		c.frame = characters[s["char"]][s["emote"]]
	textBox.text = s["String"]
	nameBox.text = s["char"].capitalize()
	
func Scene(s): # Changes the backdrop to the current scene
	for sc in $Scenes.get_children():
		sc.visible = false
	var sceneName = backdrops[s["scene"]]
	get_node("Scenes/" + sceneName).visible = true

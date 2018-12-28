extends CanvasLayer

onready var projectRes = Vector2(ProjectSettings.get_setting("display/window/size/width"), ProjectSettings.get_setting("display/window/size/height"))
onready var charNodes = get_node("Characters")
onready var textBox = get_node("TextBox/TextControl/Dialogue")
onready var nameBox = get_node("TextBox/TextControl/Name")
var choice = preload("res://Choice.tscn")

var constants
var menuDict
var positions = {}
var characters = {}
var backdrops = {}
var labels = {}
var variables = {}
var stack = []
var wait = false
var active = true

var path_to_folder = "res://output/"

func _ready():
	loadConstants("constants.json") #Only run this command when necessary!
	set_process(true)
	read("script1.json")
	jump("start")
	
func _process(delta):
	if active:
		if len(stack) > 0: #Triggers upon calling or jumping
			# get_tree().call_group("playable_characters", "hideGUI") #My games' command to hide the HUD
			get_tree().paused = true #Remove this to disable pausing upon dialogue load
			get_node("TextBox").visible = true
			if len(stack[0]) == 0:
				stack.pop_front()
			if wait:
				var statement = stack[0].pop_front()
				print(statement)
				statement(statement)
			elif Input.is_action_just_pressed("ui_select"):
				var statement = stack[0].pop_front()
				print(statement)
				statement(statement)
		elif Input.is_action_just_pressed("ui_select"):
			end()
			# get_tree().call_group("playable_characters", "showGUI") #My games' command to show the HUD
			get_tree().paused = false
	
func loadConstants(filename): # Load the constants to dictionaries for easy access
	var file = File.new()
	file.open(path_to_folder + filename, File.READ)
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
	file.open(path_to_folder + filename, File.READ) #Default filepath, you probably want to change this
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO READ FILE " + filename)
		return
	labels = data.result["labels"]
	
func statement(statement):
	match statement["action"]:
		"show":
			Show(statement)
		"hide":
			Hide(statement)
		"dialogue":
			dialogue(statement)
		"scene":
			Scene(statement)
		"call":
			call(statement["label"])
		"jump":
			jump(statement["label"])
		"var":
			variable(statement)
		"menu":
			print("Menu detected")
			menuDict = statement
			for k in statement.keys():
				if k != "action":
					option(k)
			menu()
		_:
			print("Weird flex but ok")
	
func call(label):
	wait = true
	push(label)
	print("Calling label " + label)
	
func jump(label):
	wait = true
	stack = [labels[label]]
	print("Jumping to label " + label)
	
func push(label):
	print("Adding label " + label + " to the stack.")
	stack.push_front(labels[label])
	
func pushList(l):
	print("Adding anonymous label to the stack.")
	stack.push_front(l)
	
func Show(s): # Show statement
	wait = true
	var c = charNodes.get_node(characters[s["char"]]["path"])
	c.global_position = positions[s["pos"]]
	c.frame = characters[s["char"]][s["emote"]]
	c.visible = true
	
func Hide(s): # Hide statement
	wait = true
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
	wait = false
	if s.has("emote"):
		var c = charNodes.get_node(characters[s["char"]]["path"])
		c.frame = characters[s["char"]][s["emote"]]
	textBox.text = s["String"]
	nameBox.text = s["char"].capitalize()
	
func Scene(s): # Changes the backdrop to the current scene
	wait = true
	for sc in $Scenes.get_children():
		sc.visible = false
	var sceneName = backdrops[s["scene"]]
	get_node("Scenes/" + sceneName).visible = true
		
func end():
	hideAll()
	wait = true
	yield(get_tree().create_timer(0.5), "timeout")
	# get_parent().remove_child(self) # uncomment if this is a singleton!
	
func variable(s):
	print("Assigning variable")
	wait = true
	variables[s["name"]] = s["value"]
	
func get(variable):
	return variables[variable]
	
func option(o):
	var c = choice.instance()
	$Menu.add_child(c)
	c.text = o
	c.connect("interact", self, "menu_interact", [o])
	
func menu():
	wait = true
	$Menu.visible = true
	$TextBox.visible = false
	active = false
	
func menu_interact(o):
	pushList(menuDict[o])
	$Menu.visible = false
	$TextBox.visible = true
	active = true
	for c in $Menu.get_children():
		c.queue_free()
	menuDict = {}
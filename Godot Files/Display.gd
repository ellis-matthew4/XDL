extends CanvasLayer

onready var projectRes = Vector2(ProjectSettings.get_setting("display/window/size/width"), ProjectSettings.get_setting("display/window/size/height"))
onready var charNodes = get_node("Characters")
onready var textBox = get_node("TextBox/TextControl/Dialogue")
onready var nameBox = get_node("TextBox/TextControl/Name")
var choice = preload("res://Choice.tscn") # Change this!

var menuDict
var labels = {}
var variables = {}
var stack = []
var active = true
var skip = false
var auto = false
var working = false
var able = true

var tempSave = null

var line
var TEXT_SPEED = 10
var AUTO_SPEED = 2

var path_to_folder = "res://output/" # Change this!
var currentScript
var currentScene

signal done
signal lineFinished

enum {operator, operand, leftparentheses, rightparentheses, empty}

func serialize():
	var save = {}
	save["chars"] = getCharacterStates()
	save["vars"] = variables
	save["line"] = line
	save["stack"] = stack
	save["script"] = currentScript
	save["scene"] = currentScene
	return var2str(save)
	
func deserialize(save):
	save = str2var(save)
	read(save["script"])
	Scene(save)
	variables = save["vars"]
	line = save["line"]
	stack = save["stack"]
	for c in save["chars"]:
		var t = save["chars"][c]
		get_node(c).visible = t["visible"]
		get_node(c).global_position = t["position"]
		get_node(c).play(t["emote"])
	statement()
	
func getCharacterStates():
	var d = {}
	for c in $Characters.get_children():
		var temp = {}
		temp["visible"] = c.visible
		temp["position"] = c.global_position
		temp["emote"] = c.animation
		d[get_path_to(c)] = temp
	return d

func _ready():
	read("script1.json")
	call("start")
	set_process(true)
	
func _process(delta):
	if Input.is_action_just_pressed("ui_page_up"):
		tempSave = serialize()
	if Input.is_action_just_pressed("ui_page_down"):
		if tempSave != null:
			deserialize(tempSave)
	if active:
		if len(stack) > 0: #Triggers upon calling or jumping
			# get_tree().call_group("playable_characters", "hideGUI") #My games' command to hide the HUD
			get_tree().paused = true #Remove this to disable pausing upon dialogue load
			get_node("TextBox").visible = true
			if len(stack[0]) == 0:
				stack.pop_front()
			if Input.is_action_just_pressed("ui_select"):
				nextLine()
			elif skip:
				if len(stack) > 0:
					if stack.front().front()["action"] != "menu":
						nextLine()
				else:
					end()
		elif Input.is_action_just_pressed("ui_select") and working:
			end()
			# get_tree().call_group("playable_characters", "showGUI") #My games' command to show the HUD
	if Input.is_key_pressed(KEY_CONTROL):
		skip = true
	else:
		skip = false
	
func read(filename):
	var file = File.new()
	file.open(path_to_folder + filename, File.READ)
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO READ FILE " + filename)
		return
	labels = data.result["labels"]
	currentScript = filename

func nextLine():
	if len(stack[0]) == 0:
		stack.pop_front()
	if len(stack) == 0:
		return
	line = stack[0].pop_front()
	statement()

func statement():
	if $Centered.text != "":
		$Centered.text = ""
	match line["action"]:
		"show":
			Show(line)
		"hide":
			Hide(line)
		"dialogue":
			dialogue(line)
		"adialogue":
			adialogue(line)
		"centered":
			centered(1)
		"scene":
			Scene(line)
		"call":
			call(line["label"])
		"jump":
			jump(line["label"])
		"var":
			variable(line)
		"menu":
#			print("Menu detected")
			menuDict = line
			for k in line.keys():
				if k != "action":
					option(k)
			menu()
		"window":
			window(line)
		"play":
			play(line)
		"if":
			condition(line)
		_:
			print(line)
			nextLine()
	
func call(label):
	if able:
		working = true
		push(label)
		nextLine()
	
func jump(label):
	if able:
		working = true
		stack = [labels[label].duplicate()]
		nextLine()
	
func push(label):
	var label2 = labels[label].duplicate()
	stack.push_front(label2)
	
func pushList(l):
	var l2 = l.duplicate()
	stack.push_front(l2)
	
func Show(s): # Show statement
	var c = charNodes.get_node(s["char"])
	c.global_position = $Positions.get_node(s["pos"]).global_position
	c.play(s["emote"])
	c.visible = true
	nextLine()
	
func Hide(s): # Hide statement
	var c = charNodes.get_node(s["char"])
	c.global_position = Vector2(0,0)
	c.visible = false
	nextLine()
func hideAll(): # Hides SukiGD
	get_node("TextBox").visible = false
	textBox.text = ""
	nameBox.text = ""
	for c in charNodes.get_children():
		c.global_position = Vector2(0,0)
		c.visible = false
	for sc in $Scenes.get_children():
		sc.visible = false
		
func dialogue(s): # Displays a line of dialogue
	if s.has("emote"):
		var c = charNodes.get_node(s["char"])
		c.play(s["emote"])
	$TextBox/Namebox.visible = true
	nameBox.visible = true
	nameBox.text = s["char"].capitalize()
	rollingDisplay(1)

func adialogue(s):
	$TextBox/Namebox.visible = false
	nameBox.visible = false
	rollingDisplay(1)
	
func centered(index):
	if line["action"] == "centered":
		if index <= len(line["String"]):
			$Centered.text = line["String"].substr(0,index)
			yield(get_tree().create_timer(pow(10,-TEXT_SPEED)), "timeout")
			centered(index + 1)
		else:
			emit_signal("lineFinished")
	
func rollingDisplay(index):
	if line["action"] in ["dialogue", "adialogue"]:
		if index <= len(line["String"]):
			textBox.text = line["String"].substr(0,index)
			yield(get_tree().create_timer(pow(10,-TEXT_SPEED)), "timeout")
			rollingDisplay(index + 1)
		else:
			emit_signal("lineFinished")
	
func Scene(s): # Changes the backdrop to the current scene
	for sc in $Scenes.get_children():
		sc.visible = false
	get_node("Scenes/" + s["scene"]).visible = true
	currentScene = s["scene"]
	nextLine()
		
func end():
	line = {}
	get_tree().paused = false
	hideAll()
	working = false
	emit_signal("done")
	able = false
	yield(get_tree().create_timer(0.5), "timeout")
	able = true
	
func variable(s):
	variables[s["name"]] = s["value"]
	nextLine()
	
func get(variable):
	return variables[variable]
	
func option(o):
	var c = choice.instance()
	$Menu.add_child(c)
	c.text = o
	c.connect("interact", self, "menu_interact", [o])
	
func menu():
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
	nextLine()
	
func window(s):
	if s["value"] == "hide":
		$TextBox.visible = false
	else:
		$TextBox.visible = true
	nextLine()
		
func play(s):
	$AnimationPlayer.play(s["anim"])
	nextLine()
	
func condition(s):
	var result
	match(s["opr"]):
		"==": result = expression(s["op1"]) == expression(s["op2"])
		"!=": result = expression(s["op1"]) <= expression(s["op2"])
		">=": result = expression(s["op1"]) >= expression(s["op2"])
		"!=": result = expression(s["op1"]) != expression(s["op2"])
		">": result = expression(s["op1"]) > expression(s["op2"])
		"<": result = expression(s["op1"]) < expression(s["op2"])
		_: print("ERROR! BAD OPERAND")
	if result:
		match(s["protocol"]):
			"call": call(s["target"])
			"jump": jump(s["target"])
			_: print("INVALID PROTOCOL")

func _on_root_lineFinished():
	if auto:
		yield(get_tree().create_timer(AUTO_SPEED), "timeout")
		nextLine()

func expression(pf):
	stack = []
	while len(pf) > 0:
		var c = pf.pop_front()
		if typeof(c) == operator:
			var a = stack.pop(0)
			if variables.has(a):
				a = variables[a]
			var b = stack.pop(0)
			if variables.has(b):
				b = variables[b]
			var r
			match(c):
				"+": r = a + b
				"-": r = a - b
				"*": r = a * b
				"/": r = a / b
			stack.push_front(r)
		else:
			stack.insert(0,c)
	return stack[0]
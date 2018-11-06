extends CanvasLayer

onready var projectRes = Vector2(ProjectSettings.get_setting("display/window/size/width"), ProjectSettings.get_setting("display/window/size/height"))
onready var charNodes = get_node("Characters")

var constants
var positions = {}
var characters = {}


func _ready():
	get_tree().root.connect("size_changed", self, "reloadRes")
	loadConstants("constants.json")
	read("script1.json")
	pass
	
func loadConstants(filename):
	var file = File.new()
	file.open("res://script/" + filename, File.READ)
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO LOAD FILE " + filename)
		return
	constants = data.result
	for p in constants["Positions"]:
		var pos = Vector2()
		pos.x = float(constants["Positions"][p]["x"])
		pos.y = float(constants["Positions"][p]["y"])
		positions[p] = pos * projectRes
	var temp = constants["Characters"]
	for c in temp:
		characters[c] = temp[c]
		characters[c]["path"] = characters[c]["path"].replace('"',"")
	
func read(filename):
	var file = File.new()
	file.open("res://script/" + filename, File.READ)
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO READ FILE " + filename)
		return
	data = data.result["dialogue"]
	for statement in data:
		print(statement)
		if statement["action"] == "show":
			Show(statement)
		elif statement["action"] == "hide":
			Hide(statement)
#		elif statement["action"] == "dialogue":
#			dialogue(statement)
			
func Show(s): # 
	var c = charNodes.get_node(characters[s["char"]]["path"])
	c.global_position = positions[s["pos"]]
	c.frame = characters[s["char"]][s["emote"]]
	c.visible = true
	
func Hide(s):
	var c = charNodes.get_node(characters[s["char"]]["path"])
	c.global_position = Vector2(0,0)
	c.visible = false
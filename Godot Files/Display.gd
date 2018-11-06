extends CanvasLayer

onready var positions = get_node("Positions")
onready var characters = get_node("Characters")

var constants

func _ready():
	loadConstants("constants.json")
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
	print(constants)
	
func read(filename):
	var file = File.new()
	file.open("res://script/" + filename, File.READ)
	var data = file.get_as_text()
	file.close()
	data = JSON.parse(data)
	if data.error != OK:
		print("FAILED TO READ FILE " + filename)
		return
	data = data.result
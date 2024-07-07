extends TextureButton

var text : set = setText

signal interact

func _ready():
  pass
  
func setText(text):
  $Label.text = text

func _on_Choice_pressed():
  emit_signal("interact")

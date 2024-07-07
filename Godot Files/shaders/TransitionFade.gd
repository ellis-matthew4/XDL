extends CanvasLayer

signal faded

func _ready():
	$AnimationPlayer.play("FADEOUT")
	await get_tree().create_timer(1.0).timeout
	emit_signal("faded")
	$AnimationPlayer.play("FADEIN")
	await get_tree().create_timer(0.5).timeout
	get_parent().remove_child(self)
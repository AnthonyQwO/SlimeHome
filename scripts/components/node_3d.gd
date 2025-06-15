extends Node3D

@export var character_scene: PackedScene
var character_instance

func _ready() -> void:
	character_instance = character_scene.instantiate()
	add_child(character_instance)

func _process(delta: float) -> void:
	if character_instance:
		var dir = Vector2(1, 0)  # 右移
		character_instance.move_character(dir)

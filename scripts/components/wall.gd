extends Node3D

@export_enum("None", "Left", "Right") var wall_class: int
@onready var windows = %Window
@onready var flag = true

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

#func _on_area_3d_body_entered(body: Node3D) -> void:
	#print("Enter!")
	#if wall_class == 1:
		#windows.left()
	#if wall_class == 2:
		#windows.right()


func _on_area_3d_body_exited(body: Node3D) -> void:
	print("Exit!")
	windows.stop()
	flag = true

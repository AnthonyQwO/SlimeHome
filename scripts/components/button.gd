extends Button

@onready var host = $"../HTTPRequest"
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _on_pressed() -> void:
	host.send_messenge()
	print("按鈕已被按下，發送訊息")

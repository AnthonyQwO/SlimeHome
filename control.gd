extends Control

@onready var input_box = $LineEdit

func _ready():
	input_box.placeholder_text = "請輸入文字"
	input_box.text = ""

func _on_LineEdit_text_submitted(new_text):
	print("使用者輸入：", new_text)

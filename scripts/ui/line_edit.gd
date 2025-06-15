extends LineEdit

@export var diolog: RichTextLabel
@export var http_host: HTTPRequest

func _ready() -> void:
	placeholder_text = "請輸入文字..."
	text_submitted.connect(_on_text_submitted)

func _on_text_submitted(new_text: String) -> void:
	print("使用者輸入：", new_text)
	diolog._add_text("：" + new_text)
	http_host.send_messenge(new_text)
	text = ""

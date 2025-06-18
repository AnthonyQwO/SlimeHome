extends Node

var http_request: HTTPRequest

@export var diolog: RichTextLabel
@onready var ch = $"../../../Charater"

func _ready():
	pass
	
func send_messenge(messenge: String):
	# 建立 HTTPRequest 節點並連接信號
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)

	# 生成測試狀態資料
	var state = generate_test_state(ch.position, messenge)

	# 將資料轉換為 JSON 字串
	var json_body = JSON.stringify(state)

	# 設定標頭
	var headers = ["Content-Type: application/json"]

	# 發送 POST 請求
	var error = http_request.request("http://localhost:8000/api/test", headers, HTTPClient.METHOD_POST, json_body)
	
	print("Send: " + messenge)
	if error != OK:
		push_error("HTTP 請求發生錯誤，錯誤碼: %d" % error)

func generate_test_state(pos: Vector3, messenge: String) -> Dictionary:
	return {
		"current_state": "idle",
		"duration": 10,
		"position": {"x": pos.x, "y": pos.y, "z": pos.z},
		"hunger": 5,
		"happiness": 10,
		"food_present": true,
		"food_position": {"x": 35, "y": 0, "z": 15},
		"recent_actions": ["idle", "walk", "idle"],
		"current_input": messenge
	}

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var response_text = body.get_string_from_utf8()
		var json_result = JSON.parse_string(response_text)
		if json_result != null:
			print("後端回應:")
			print(JSON.stringify(json_result, "\t"))
			
			var narration = json_result["narration"]
			var targetX = json_result["params"]["targetX"]
			var targetZ = json_result["params"]["targetZ"]
			
			print("敘述：", narration)
			print(targetX, targetZ)
			
			diolog._add_text(narration)
			
			if targetX != null and targetZ != null:
				ch.navigate_to_position(Vector3(float(targetX), 0, float(targetZ)))
		else:
			push_error("無法解析 JSON 回應")
	else:
		push_error("HTTP 回應錯誤，狀態碼: %d" % response_code)

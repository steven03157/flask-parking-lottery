from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 模擬社區住戶門號（可以根據實際情況修改）
residents = {str(i): None for i in range(101, 226)}  # 101~225 號住戶
parking_slots = list(range(1, 126))  # 125 個停車位
random.shuffle(parking_slots)  # 隨機排列停車位

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>停車位抽選</title>
        <script>
            async function drawParking() {
                const doorNumber = document.getElementById("door_number").value;
                const response = await fetch("/draw", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ door_number: doorNumber })
                });
                const result = await response.json();
                document.getElementById("result").innerText = result.message;
            }
        </script>
    </head>
    <body>
        <h1>社區大樓停車位抽選</h1>
        <label for="door_number">輸入您的門號：</label>
        <input type="text" id="door_number" placeholder="例如：101">
        <button onclick="drawParking()">抽選</button>
        <p id="result"></p>
    </body>
    </html>
    '''

@app.route('/draw', methods=['POST'])
def draw():
    door_number = request.json.get('door_number')
    
    if door_number not in residents:
        return jsonify({'status': 'error', 'message': '無效的門號'}), 400
    
    if residents[door_number] is not None:
        return jsonify({'status': 'error', 'message': f'您已抽中停車位 {residents[door_number]}'}), 400
    
    if not parking_slots:
        return jsonify({'status': 'error', 'message': '停車位已被抽完'}), 400
    
    assigned_slot = parking_slots.pop()
    residents[door_number] = assigned_slot
    return jsonify({'status': 'success', 'message': f'恭喜！您的停車位是 {assigned_slot}'})

if __name__ == '__main__':
    app.run(debug=True)
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # 取得 Render 指定的 PORT，預設 5000
    app.run(host='0.0.0.0', port=port)

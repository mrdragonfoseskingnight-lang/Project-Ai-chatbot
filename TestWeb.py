from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

# เริ่มต้นไคลเอนต์ OpenAI
client = OpenAI(
    api_key=os.environ.get("sk-yuzgnijn1KdGLcDExLOMPPPpZZYkuIdfujrczFAY0I3UPtdG"),
    base_url="https://playground.opentyphoon.ai/"
)

# เทมเพลต HTML อย่างง่ายสำหรับอินเตอร์เฟซแชท
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Thai Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        #chat-container { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; }
        .user-message { background-color: #e6f7ff; padding: 8px; border-radius: 10px; margin: 5px 0; text-align: right; }
        .assistant-message { background-color: #f0f0f0; padding: 8px; border-radius: 10px; margin: 5px 0; text-align: left; }
        #user-input { width: 85%; padding: 8px; }
        button { padding: 8px 15px; }
    </style>
</head>
<body>
    <h1>ผู้ช่วยภาษาไทย</h1>
    <div id="chat-container"></div>
    <div>
        <input type="text" id="user-input" placeholder="พิมพ์ข้อความของคุณ..." />
        <button onclick="sendMessage()">ส่ง</button>
    </div>
    <script>
        function addMessageToChat(content, isUser) {
            const chatContainer = document.getElementById('chat-container');
            const messageDiv = document.createElement('div');
            messageDiv.className = isUser ? 'user-message' : 'assistant-message';
            messageDiv.innerText = content;
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }

        async function sendMessage() {
            const userInput = document.getElementById('user-input');
            const userMessage = userInput.value.trim();

            if (!userMessage) return;

            addMessageToChat(userMessage, true);
            userInput.value = '';

            // แสดงตัวบ่งชี้กำลังคิด
            const thinkingDiv = document.createElement('div');
            thinkingDiv.className = 'assistant-message';
            thinkingDiv.id = 'thinking';
            thinkingDiv.innerText = 'กำลังคิด...';
            document.getElementById('chat-container').appendChild(thinkingDiv);

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: userMessage})
                });

                const data = await response.json();

                // ลบตัวบ่งชี้กำลังคิด
                document.getElementById('thinking').remove();

                addMessageToChat(data.response, false);
            } catch (error) {
                document.getElementById('thinking').remove();
                addMessageToChat('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง', false);
                console.error('Error:', error);
            }
        }

        // กดปุ่ม Enter เพื่อส่ง
        document.getElementById('user-input').addEventListener('keyup', function(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')

    try:
        response = client.chat.completions.create(
            model="typhoon-v2.1-12b-instruct",
            messages=[
                {"role": "system", "content": "คุณเป็นผู้ช่วยที่เป็นมิตรและให้ข้อมูลที่เป็นประโยชน์แก่ผู้ใช้ คุณจะตอบคำถามเป็นภาษาไทยที่สุภาพและเข้าใจง่าย"},
                {"role": "user", "content": user_message}
            ],
            max_tokens=512,
            temperature=0.7
        )

        return jsonify({"response": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
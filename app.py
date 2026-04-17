from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# Mengizinkan Vercel (Frontend) berkomunikasi dengan server ini tanpa diblokir browser
CORS(app)

# Menarik API Keys dari "Brankas Rahasia" (Environment Variables)
SHODAN_API = os.getenv("SHODAN_API_KEY", "Tidak Ada API Key")
FACE_API = os.getenv("FACE_API_KEY", "Tidak Ada API Key")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Silentium Engine is Online", "mode": "Hybrid-Ready"})

@app.route('/api/osint', methods=['POST'])
def run_osint():
    data = request.json
    search_type = data.get('type')
    target = data.get('target')
    
    response_data = {"status": "success", "target": target, "results": ""}
    
    # --- MODUL USERNAME ---
    if search_type == 'username':
        # Simulasi pencarian cepat (Bisa dikembangkan dengan request sesungguhnya)
        github_check = requests.get(f"https://api.github.com/users/{target}")
        if github_check.status_code == 200:
            response_data["results"] += "[-] GitHub: Active Profile Found\n"
        else:
            response_data["results"] += "[x] GitHub: No trace\n"
        response_data["results"] += f"[-] API Key Status: Aman (Shodan: {SHODAN_API[:4]}***)"
        
    # --- MODUL IP / NETWORK ---
    elif search_type == 'ip':
        try:
            res = requests.get(f"http://ip-api.com/json/{target}").json()
            if res.get("status") == "success":
                response_data["results"] += f"[-] ISP: {res.get('isp')}\n[-] City: {res.get('city')}\n[-] Lat/Lon: {res.get('lat')}/{res.get('lon')}"
            else:
                response_data["results"] = "[x] Invalid IP or Local Network"
        except:
            response_data["results"] = "[x] Network Error"

    # --- MODUL FACE / IMAGE (Simulasi) ---
    elif search_type == 'face':
        response_data["results"] = "[-] Face structure analyzed.\n[-] Database match: 78%\n[-] Note: Membutuhkan Face API Key valid untuk data real."
        
    else:
        response_data["results"] = "[!] Modul tidak dikenali."

    return jsonify(response_data)

if __name__ == '__main__':
    # Berjalan di port 5000 secara default
    app.run(host='0.0.0.0', port=5000)

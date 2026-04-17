from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
# Mengizinkan Web Vercel berkomunikasi dengan server ini
CORS(app)

# Menarik API Keys dari Environment Variables (Brankas Rahasia)
# Jika kunci belum di-inject, nilainya akan kosong ("")
SHODAN_API = os.getenv("SHODAN_API_KEY", "")
VT_API = os.getenv("VIRUSTOTAL_API", "")
EMAILREP_API = os.getenv("EMAILREP_API", "")
CRIMINAL_IP_API = os.getenv("CRIMINAL_IP_API", "")

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Silentium Engine is Online", "modules": "Hybrid-Ready"})

@app.route('/api/osint', methods=['POST'])
def run_osint():
    data = request.json
    search_type = data.get('type')
    target = data.get('target')
    
    # Template respon bawaan untuk Web GUI
    response_data = {
        "status": "success", 
        "target": target, 
        "results": "",
        "lat": None,
        "lon": None,
        "chart_data": [10, 10, 10, 10, 10] # Baseline statistik untuk radar chart
    }
    
    # --- MODUL IP ADDRESS ---
    if search_type == 'ip':
        # 1. IP Geo-Location (Gratis, Tanpa Key)
        try:
            geo = requests.get(f"http://ip-api.com/json/{target}").json()
            if geo.get("status") == "success":
                response_data["lat"] = geo.get('lat')
                response_data["lon"] = geo.get('lon')
                response_data["results"] += f"[-] ISP: {geo.get('isp')}\n[-] Lokasi: {geo.get('city')}, {geo.get('country')}\n"
                response_data["chart_data"] = [80, 40, 60, 90, 50] # Simulasi data metrik jaringan
            else:
                response_data["results"] += "[x] Gagal melacak kordinat IP.\n"
        except:
            response_data["results"] += "[x] Gangguan koneksi ke IP-API.\n"
            
        # 2. VirusTotal (Jika Key sudah di-inject)
        if VT_API:
            headers = {"x-apikey": VT_API}
            vt_res = requests.get(f"https://www.virustotal.com/api/v3/ip_addresses/{target}", headers=headers)
            if vt_res.status_code == 200:
                malicious = vt_res.json()['data']['attributes']['last_analysis_stats']['malicious']
                response_data["results"] += f"[-] VirusTotal Threat Score: {malicious} engines detected malicious\n"
            else:
                response_data["results"] += "[!] VirusTotal API Limit atau Error.\n"
        else:
            response_data["results"] += "[!] VirusTotal API Key kosong. Melewati pemindaian ancaman.\n"

    # --- MODUL EMAIL ---
    elif search_type == 'email':
        if EMAILREP_API:
            headers = {"Key": EMAILREP_API}
            em_res = requests.get(f"https://emailrep.io/{target}", headers=headers)
            if em_res.status_code == 200:
                em_data = em_res.json()
                rep = em_data.get('reputation', 'unknown')
                response_data["results"] += f"[-] Reputasi Email: {rep}\n[-] Data Tersebar di Internet: {em_data.get('references', 0)} sumber\n"
                response_data["chart_data"] = [20, 80, 70, 40, 90]
            else:
                response_data["results"] += "[!] EmailRep koneksi ditolak.\n"
        else:
            response_data["results"] += "[!] EmailRep API Key kosong. Membutuhkan kunci untuk OSINT Email.\n"

    # --- MODUL USERNAME ---
    elif search_type == 'username':
        # Pencarian Github sebagai dasar
        github_check = requests.get(f"https://api.github.com/users/{target}")
        if github_check.status_code == 200:
            response_data["results"] += "[-] Github: Aktif / Ditemukan\n"
            response_data["chart_data"] = [50, 90, 80, 30, 70]
        else:
            response_data["results"] += "[x] Github: Tidak ada jejak\n"
        response_data["results"] += "[-] Menunggu integrasi Sherlock lokal...\n"

    else:
        response_data["results"] = "[x] Parameter tidak dikenali."

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

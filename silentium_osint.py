import requests
import json
import sys

def print_banner():
    print(r"""
  ____  _ _            _   _                 ___  ____ ___ _   _ _____ 
 / ___|(_) | ___ _ __ | |_(_)_   _ _ __ ___ / _ \/ ___|_ _| \ | |_   _|
 \___ \| | |/ _ \ '_ \| __| | | | | '_ ` _ \ | | \___ \| ||  \| | | |  
  ___) | | |  __/ | | | |_| | |_| | | | | | | |_| |___) | || |\  | | |  
 |____/|_|_|\___|_| |_|\__|_|\__,_|_| |_| |_|\___/|____/___|_| \_| |_|  
           [ Multi-Module Recon | Kenzokens Terminal ]
    """)

def check_username(username):
    print(f"\n[+] Memindai jejak digital untuk target: {username}...")
    # Daftar situs target (Bisa kamu tambah sendiri nanti)
    sites = {
        "GitHub": f"https://api.github.com/users/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Pinterest": f"https://id.pinterest.com/{username}/",
        "Medium": f"https://medium.com/@{username}"
    }
    
    for site, url in sites.items():
        try:
            # Fake User-Agent agar tidak mudah diblokir firewall
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                print(f"    [FOUND] {site} : Aktif")
            elif response.status_code == 404:
                print(f"    [MISS]  {site} : Tidak ditemukan")
            else:
                print(f"    [INFO]  {site} : Membutuhkan verifikasi manual (Status {response.status_code})")
        except requests.exceptions.RequestException:
            print(f"    [ERR]   {site} : Koneksi terputus")

def check_ip(ip_address):
    print(f"\n[+] Membedah informasi jaringan untuk IP: {ip_address}...")
    try:
        # Menggunakan API publik gratis tanpa key
        res = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        if res.get("status") == "success":
            print(f"    [!] Provider : {res.get('isp')}")
            print(f"    [!] Organisasi: {res.get('org')}")
            print(f"    [!] Lokasi   : {res.get('city')}, {res.get('country')}")
            print(f"    [!] Zona Waktu: {res.get('timezone')}")
            print(f"    [!] Koordinat: Lat {res.get('lat')} / Lon {res.get('lon')}")
        else:
            print("    [X] IP tidak valid atau terdeteksi sebagai local network.")
    except Exception as e:
        print(f"    [X] Gagal melacak jaringan: {e}")

if __name__ == "__main__":
    print_banner()
    print("Pilih modul operasi intelijen:")
    print("1. Lacak Jejak Username (Footprinting)")
    print("2. Analisa IP Address (Network Recon)")
    print("0. Keluar")
    
    try:
        choice = input("\n[?] Masukkan nomor modul (1/2/0): ")
        
        if choice == '1':
            target = input("[-] Masukkan username target: ")
            check_username(target)
        elif choice == '2':
            target = input("[-] Masukkan alamat IP target: ")
            check_ip(target)
        elif choice == '0':
            print("\nShutting down terminal... Goodbye.")
            sys.exit()
        else:
            print("\n[!] Perintah tidak dikenali.")
    except KeyboardInterrupt:
        print("\n\n[!] Operasi dibatalkan oleh user. Exiting...")
        sys.exit()

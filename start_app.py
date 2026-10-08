import http.server
import socketserver
import webbrowser
import os
import sys
import json
import socket

PORT = 8000

# Change working directory to the directory where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_local_ip():
    """Detect LAN IPv4 address (e.g. 192.168.x.x) for local network access"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return '127.0.0.1'

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS and caching headers for local media
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/server_info':
            local_ip = get_local_ip()
            info = {
                'success': True,
                'local_ip': local_ip,
                'port': PORT,
                'local_url': f"http://localhost:{PORT}/index.html",
                'lan_url': f"http://{local_ip}:{PORT}/index.html",
                'lan_page': f"http://{local_ip}:{PORT}/lan.html"
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(info, ensure_ascii=False).encode('utf-8'))
            return
        super().do_GET()

    def do_POST(self):
        if self.path == '/api/save_question':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                body = self.rfile.read(content_length)
                payload = json.loads(body.decode('utf-8'))
                
                qid = payload.get('id')
                skill = payload.get('skill', 'listening')
                correct_ans = payload.get('correctAnswer')
                exp = payload.get('explanation')
                
                target_json = 'toeic_app_data.json' if skill == 'listening' else 'toeic_reading_data.json'
                target_js = 'toeic_app_data.js' if skill == 'listening' else 'toeic_reading_data.js'
                js_var = 'window.TOEIC_DATA' if skill == 'listening' else 'window.TOEIC_READING_DATA'
                
                if os.path.exists(target_json):
                    with open(target_json, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    for q in data:
                        if q.get('id') == qid:
                            if correct_ans:
                                q['correctAnswer'] = correct_ans
                            if exp is not None:
                                q['explanation'] = exp
                            break
                    
                    with open(target_json, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    with open(target_js, 'w', encoding='utf-8') as f:
                        f.write(f"{js_var} = {json.dumps(data, ensure_ascii=False)};\n")
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'id': qid}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
                return
        
        self.send_response(404)
        self.end_headers()

def run():
    sys.stdout.reconfigure(encoding='utf-8')
    global PORT
    local_ip = get_local_ip()
    for attempt in range(10):
        try:
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                url_local = f"http://localhost:{PORT}/index.html"
                url_lan = f"http://{local_ip}:{PORT}/index.html"
                url_lan_portal = f"http://{local_ip}:{PORT}/lan.html"
                print("=" * 68)
                print("   TOEIC MASTER B1 - SERVER DANG HOAT DONG!")
                print("=" * 68)
                print(f"   * May tinh nay (Localhost) : {url_local}")
                print(f"   * Mang noi bo / Wi-Fi (LAN): {url_lan}")
                print(f"   * Huong dan ket noi LAN    : {url_lan_portal}")
                print("-" * 68)
                print("   Luu y ket noi dien thoai / iPad / Laptop:")
                print("   1. Ket noi cung mang Wi-Fi voi may tinh nay.")
                print(f"   2. Mo trinh duyet tren dien thoai va truy cap: {url_lan}")
                print("   Nhan Ctrl + C de dung may chu.")
                print("=" * 68)
                webbrowser.open(url_local)
                httpd.serve_forever()
        except OSError:
            PORT += 1

if __name__ == "__main__":
    run()

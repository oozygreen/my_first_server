# branch lv.3

from http.server import HTTPServer, BaseHTTPRequestHandler
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)

CLIENT_DIR = os.path.join(root_dir, 'client')

TEMPLATE_CACHE = {}

def load_templates():
    print("--- [System] 템플릿 및 정적 파일을 메모리에 로드합니다 (I/O 최소화) ---")
    
    files_to_load = {
        'index': 'index.html',
        'header': 'page/header.html',
        'body': 'page/body.html',
        'footer_default': 'page/footer.html',
        'footer_01': 'page/bottom/footer01.html',
        'footer_02': 'page/bottom/footer02.html',
        'footer_03': 'page/bottom/footer03.html',
        'footer_04': 'page/bottom/footer04.html',
        'footer_05': 'page/bottom/footer05.html',
        'css_main': 'css/style.css', 
        '404': '404error.html'
    }

    file_contents = {}
    for key, path in files_to_load.items():
        full_path = os.path.join(CLIENT_DIR, path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                file_contents[key] = f.read()
                print(f"[OK] {key} 로드 완료")
        except FileNotFoundError:
            print(f"[Warning] 파일을 찾을 수 없습니다: {full_path}")
            file_contents[key] = ""

    base_html = file_contents['index']
    base_html = base_html.replace('{{header}}', file_contents['header'])
    base_html = base_html.replace('{{body}}', file_contents['body'])
    
    TEMPLATE_CACHE['base_layout'] = base_html
    
    for key, content in file_contents.items():
        if key not in ['index', 'header', 'body']:
            TEMPLATE_CACHE[key] = content

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # [기존 코드 주석처리] 로그 출력은 유지
        print(f"요청 메서드: {self.command}")
        print(f"요청 경로: {self.path}")
        print(f"요청 헤더: \n{self.headers}")

        path = self.path

        if path.endswith('.css'):
            content = TEMPLATE_CACHE.get('css_main', '')
            
            if content:
                self.send_response(200)
                self.send_header('Content-type', 'text/css; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, "CSS File Not Found in Cache")
            return

        footer_mapping_keys = {
            '/': 'footer_default',
            '/01': 'footer_01',
            '/02': 'footer_02',
            '/03': 'footer_03',
            '/04': 'footer_04',
            '/05': 'footer_05',
        }

        content = TEMPLATE_CACHE.get('base_layout', '')

        if path not in footer_mapping_keys and path != '/':
            error_content = TEMPLATE_CACHE.get('404', '<h1>404 Not Found</h1>')
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(error_content.encode('utf-8'))
            return

        footer_key = footer_mapping_keys.get(path, 'footer_default')
        footer_content = TEMPLATE_CACHE.get(footer_key, '')

        content = content.replace('{{footer}}', footer_content)


        print(f"\n--- [Server Response Out] ---")
        print(f"상태 코드(Status): 200")
        print(f"대상 경로(Path): {path}")
        print(f"컨텐츠 타입(Content-Type): text/html")
        print(f"-----------------------------\n")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

host = 'localhost'
port = 7777

load_templates()

server = HTTPServer((host, port), MyRequestHandler)

try:
    print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
    print("종료하려면 터미널에서 Ctrl+C를 누르세요.")
    server.serve_forever()
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()
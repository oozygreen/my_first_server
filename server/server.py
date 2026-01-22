from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# 1. 전역 캐시
TEMPLATE_CACHE = {}

def load_templates():
    print("--- 템플릿 파일을 메모리에 로드하고 조립합니다 ---")
    # 1) 파일 읽기 (기존과 동일)
    raw_files = {
        'index': 'client/index.html',
        'header': 'client/page/header.html',
        'body': 'client/page/body.html',
        'footer_default': 'client/page/footer.html',
        'footer_01': 'client/page/bottom/footer01.html',
        'footer_02': 'client/page/bottom/footer02.html',
        'footer_03': 'client/page/bottom/footer03.html',
        'footer_04': 'client/page/bottom/footer04.html',
        'footer_05': 'client/page/bottom/footer05.html',
        '404error': 'client/404error.html',
        'style': 'client/css/style.css'
    }
    
    file_contents = {}
    for key, path in raw_files.items():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                file_contents[key] = f.read()
        except FileNotFoundError:
            file_contents[key] = ""

    # 2) [핵심] 여기서 미리 조립합니다! (Pre-assembling)
    # index + header + body는 항상 똑같으므로 미리 합쳐서 'base_layout'이라는 이름으로 저장합니다.
    # 단, {{footer}} 부분은 아직 어떤 푸터가 올지 모르니 그대로 둡니다.
    
    base_html = file_contents['index']
    base_html = base_html.replace('{{header}}', file_contents['header'])
    base_html = base_html.replace('{{body}}', file_contents['body'])
    
    # 조립된 덩어리를 캐시에 저장
    TEMPLATE_CACHE['base_layout'] = base_html
    
    # 푸터들은 나중에 골라 써야 하므로 각각 따로 캐시에 저장
    TEMPLATE_CACHE['footer_default'] = file_contents['footer_default']
    TEMPLATE_CACHE['footer_01'] = file_contents['footer_01']
    TEMPLATE_CACHE['footer_02'] = file_contents['footer_02']
    TEMPLATE_CACHE['footer_03'] = file_contents['footer_03']
    TEMPLATE_CACHE['footer_04'] = file_contents['footer_04']
    TEMPLATE_CACHE['footer_05'] = file_contents['footer_05']

    # 404에러 페이지를 캐시에 저장
    TEMPLATE_CACHE['404error'] = file_contents['404error']



class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(f"요청 메서드: {self.command}")
        print(f"요청 경로: {self.path}")
        print(f"요청 헤더: \n{self.headers}")

        path = self.path
        
        # 2. 라우팅 로직 처리
        # 사용자가 요청한 path가 매핑 테이블에 있다면, index.html을 기본 틀로 사용합니다.
        is_dynamic_route = path in footer_map
        
        if is_dynamic_route or path == '/':
            file_path = 'client/index.html'
        else:
            file_path = f'client{path}'

        # 3. 확장자 및 Content-Type 결정
        if file_path.endswith('.html'):
            content_type = 'text/html'
        elif file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.js'):
            content_type = 'application/javascript'
        else:
            content_type = 'text/plain'

        # 4. 응답 생성
        try:
            # HTML 파일인 경우 (템플릿 엔진 로직 실행)
            if file_path == 'client/index.html':
                # 틀이 되는 index.html 읽기
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 공통 컴포넌트 읽기
                with open('client/page/header.html', 'r', encoding='utf-8') as h:
                    header_content = h.read()
                with open('client/page/body.html', 'r', encoding='utf-8') as b:
                    body_content = b.read()

                # [핵심] 경로에 맞는 푸터 결정 (없으면 기본 footer.html)
                footer_target = footer_map.get(path, 'client/page/footer.html')
                with open(footer_target, 'r', encoding='utf-8') as f_low:
                    footer_content = f_low.read()

                # 템플릿 치환
                content = content.replace('{{header}}', header_content)
                content = content.replace('{{body}}', body_content)
                content = content.replace('{{footer}}', footer_content)

                # index.html 하단에 </body> 태그 직전에 스크립트를 삽입하도록 설정합니다.
                console_script = "<script>console.log('응답을 받았습니다: 서버 사이드에서 보낸 메시지');</script>"
                content = content.replace('</body>', f'{console_script}</body>')

                # [추가] 서버 터미널에서 응답 확인을 위한 로그 출력
                print(f"\n--- [Server Response Out] ---")
                print(f"상태 코드(Status): {self.responses[200][0] if file_path == 'client/index.html' else '200'}") 
                print(f"대상 경로(Path): {path}")
                print(f"컨텐츠 타입(Content-Type): {content_type if 'content_type' in locals() else 'text/html'}")
                print(f"주입된 스크립트 존재 여부: {'Yes' if 'console_script' in locals() else 'No'}")
                print(f"-----------------------------\n")
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))

            # 그 외 정적 파일(CSS, JS 등) 처리
            else:
                with open(file_path, 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', f'{content_type}; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(content)

        except FileNotFoundError:
            self.send_error_page(file_path)

    def send_error_page(self, file_path):
        try:
            with open('client/404error.html', 'r', encoding='utf-8') as f:
                error_content = f.read()
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(error_content.encode('utf-8'))
        except:
            self.send_error(404, f"File Not Found: {file_path}")

# 서버 실행부 (기존과 동일)
host = 'localhost'
port = 7777

server = HTTPServer((host, port), MyRequestHandler)

try:
    print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
    print("종료하려면 터미널에서 Ctrl+C를 누르세요.")
    server.serve_forever()
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()
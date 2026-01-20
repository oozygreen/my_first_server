from http.server import HTTPServer, BaseHTTPRequestHandler

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # 1. 동적 푸터 매핑 테이블 (데이터 중심 설계)
        # 경로(Key)에 따라 읽어올 파일(Value)을 지정합니다.
        footer_map = {
            '/': 'client/page/footer.html',
            '/01': 'client/page/bottom/footer01.html',
            '/02': 'client/page/bottom/footer02.html',
            '/03': 'client/page/bottom/footer03.html',
            '/04': 'client/page/bottom/footer04.html',
            '/05': 'client/page/bottom/footer05.html',
        }

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
print(f"서버 시작: http://{host}:{port}")
server.serve_forever()
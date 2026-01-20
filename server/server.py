from http.server import HTTPServer, BaseHTTPRequestHandler

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. 경로 결정 (Routing)
        path = self.path
        # self.path는 요청된 URL의 경로 부분을 나타냄

        if path == '/':
            path = '/index.html'
        # 만약 경로가 기본페이지('/)라면 index.html을 보여주도록 설정
        
        file_path = f'client{path}'
        # 실제 파일 경로 설정(실게 서버 컴퓨터 내의 폴더 경로와 사용자가 요청한 경로를 조합)
        # 결과값은 'client/index.html', 'client/css/style.css' 등으로 설정됨

        # 2. 확장자에 따른 Content-Type 결정
        # 브라우저에게 서버가 보내는 데이터가 어떤 종류의 파일인지 알려주기 위함
        if file_path.endswith('.html'):
            content_type = 'text/html'
        elif file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.js'):
            content_type = 'application/javascript'
        else:
            # 지정되지 않은 확장자는 모두 일반 텍스트로 처리
            content_type = 'text/plain'

        # 3. 파일 읽기 및 전송
        try:
            if file_path.endswith('.html'):
                with open(file_path, 'r', encoding='utf-8') as f:
                # 만약 파일이 HTML일 경우, 내용을 조립해야 하므로 텍스트 모드('r')로 열기
                    content = f.read()
                    # 파일 객체 f가 가리키고 있는 데이터 전체를 읽어서 메모리(RAM)로 로드해서 content 변수에 저장

                # index.html일 경우에 분리된 조각 파일들을 조립
                if file_path == 'client/index.html':
                    # 각 컴포넌트 파일(header, body, footer)을 읽어와 각각의 변수에 저장
                    with open('client/html/header.html', 'r', encoding='utf-8') as h:
                        header_content = h.read()
                    with open('client/html/body.html', 'r', encoding='utf-8') as b:
                        body_content = b.read()
                    with open('client/html/footer.html', 'r', encoding='utf-8') as f_low:
                        footer_content = f_low.read()

                    # 메인 파일(index.html) 내의 예약어({{...}})를 실제 파일 내용으로 갈아끼움
                    content = content.replace('{{header}}', header_content)
                    content = content.replace('{{body}}', body_content)
                    content = content.replace('{{footer}}', footer_content)

                # 최종 조립된 HTML 전송
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            
            # HTML 외의 파일(CSS, JS, 이미지 등)은 내용 수정 없이 원본 그대로 보냄
            else:
                with open(file_path, 'rb') as f:
                # 바이너리 읽기 모드('rb')로 읽어 별도의 인코딩 과정 없이 데이터 덩어리 자체를 가져옵니다.
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', f'{content_type}; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(content)

        # 만약 요청한 경로에 실제 파일이 존재하지 않는 경우 예외 처리를 수행 
        except FileNotFoundError:
            # 1. 지정된 404 페이지 파일을 읽어옵니다. (인코딩 필수!)
            try:
                with open('client/404error.html', 'r', encoding='utf-8') as f:
                    error_content = f.read()
                
                # 2. HTTP 응답 형식을 갖춰서 전송합니다.
                self.send_response(404) # 상태 코드는 당연히 404!
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(error_content.encode('utf-8'))
                
            except Exception as e:
                # 만약 404 페이지 파일 자체를 못 찾는 비상 사태라면?
                # 이때는 브라우저 기본 에러 메시지를 보냅니다.
                self.send_error(404, f"File Not Found: {file_path}")

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
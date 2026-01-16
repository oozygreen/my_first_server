from http.server import HTTPServer, BaseHTTPRequestHandler
# http.server라는 표준 라이브러리에서 HTTPServer와 BaseHTTPRequestHandler 클래스를 임포트

class MyRequestHandler(BaseHTTPRequestHandler):
# BaseHTTPRequestHandler라는 부모 클래스를 상속받아 MyRequestHandler라는 새로운 클래스를 정의
# BaseHTTPRequestHandler에서 요청을 받으면 처리는 MyRequestHandler 클래스의 매뉴얼을 따르도록 함
    def do_GET(self):
    # do_GET 의 이름은 BaseHTTPRequestHandler 클래스에서 미리 정의된 메서드 이름이므로 변경하면 안 됨
    # 클라이언트가 GET 요청을 보낼 때마다 이 메서드가 호출됨

        # ---------- 기본 서버 구동 로직 ----------
        #self.send_response(200)
        # 200은 성공을 의미하는 HTTP 상태 코드
        # if문 등으로 요청 경로에 따라 다른 응답을 보내도록 확장할 수 있음
        # self.send_header('Content-type', 'text/html; charset=utf-8')
        # 응답 헤더 설정, 여기서는 콘텐츠 타입을 HTML로 지정(UTF-8 인코딩 포함)
        # self.end_headers()
        # 헤더 설정이 끝났음을 알림
        # message = "<h1>안녕하세요! 파이썬 서버입니다.</h1>"
        # 응답 본문 설정 -> 현재 서버 구동 확인용으로 간결하게 작성했지만 추후 HTML 파일을 읽어와서 응답할 예정
        # self.wfile.write(message.encode('utf-8'))
        # 응답 본문을 클라이언트로 전송, 문자열을 바이트로 인코딩하여 전송
        # -----------------------------------------

        # ---------- 클라이언트 UI 출력을 위한 고도화 및 404에러 예외처리 ----------
        if self.path == '/':
            file_path = 'client/index.html'
        else:
            file_path = 'client/404error.html'

        content_type = 'text/plain'
        if file_path.endswith('.html'):
            content_type = 'text/html'

        try:
            # 파일 읽기 및 응답 전송
            with open(file_path, 'rb') as f:
                # 'rb' (read binary) 모드는 텍스트와 이미지 모두 처리가 가능
                content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', f'{content_type}; charset=utf-8')
                self.end_headers()
                self.wfile.write(content)
                
        except FileNotFoundError:
            # 파일을 찾을 수 없을 때 404 에러 응답
            self.send_error(404, f"File Not Found: {file_path}")

        
    # POST가 필요하면 def do_POST(self):를 아래에 똑같이 정의해주면 됩니다. 메서드별로 함수를 따로 생성

host = 'localhost' # 서버 호스트 주소 설정
# localhost는 전세계적으로 컴퓨터 자신을 가리키는 표준 호스트 이름
# 컴퓨터 운영체제의 hosts 파일을 직접 수정하여 localhost가 다른 IP 주소를 가리키도록 변경할 수는 있음
port = 7777 # 서버 포트 번호 설정
# 0~65535 사이의 포트 번호를 사용할 수 있지만, 1024 미만의 포트는 시스템 예약 포트이므로 피하는 것이 좋음

server = HTTPServer((host, port), MyRequestHandler)
# 클래스 상속 아님
# HTTPServer 인스턴스 생성, (호스트, 포트) 튜플과 요청 처리 핸들러 클래스를 인자로 전달


try:
    print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
    print("종료하려면 터미널에서 Ctrl+C를 누르세요.") # Ctrl+C는 표준적인 인터럽트 신호
    server.serve_forever()
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()
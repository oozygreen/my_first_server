from http.server import HTTPServer, BaseHTTPRequestHandler
import os  # [중요] 경로 계산을 위해 운영체제 모듈을 가져옵니다.

# [추가됨] 경로 설정의 기준점 잡기
# 1. 현재 실행 중인 파일(server.py)의 절대 경로를 구합니다.
#    예: C:\Users\...\server\server.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. server.py의 상위 폴더(프로젝트 루트)로 한 칸 올라갑니다.
#    예: C:\Users\...\server\..  -> C:\Users\...\프로젝트폴더
root_dir = os.path.dirname(current_dir)

# 3. 이제 'client' 폴더는 root_dir 아래에 있다고 명시합니다.
#    이렇게 하면 터미널 위치와 상관없이 정확한 위치를 찾습니다.
CLIENT_DIR = os.path.join(root_dir, 'client')


# [추가됨] 전역 변수: 파일 내용을 메모리에 저장해둘 '캐시 저장소'입니다.
# 요청이 올 때마다 디스크를 읽는 대신, 이 변수에서 꺼내 쓸 것입니다.
TEMPLATE_CACHE = {}

# [추가됨] 서버 시작 시 파일을 한 번만 읽어오는 초기화 함수
def load_templates():
    print("--- [System] 템플릿 및 정적 파일을 메모리에 로드합니다 (I/O 최소화) ---")
    
    # 1. 읽어올 파일들의 경로 정의
    # (CSS 파일명이 style.css라고 가정했습니다. 실제 파일명에 맞춰 수정해주세요)
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
        # [CSS 캐싱 추가] CSS 파일도 문자열이므로 미리 읽어둡니다.
        'css_main': 'css/style.css', 
        '404': '404error.html'
    }

    # 2. 파일 읽어서 캐시에 저장
    file_contents = {}
    for key, path in files_to_load.items():
        # [수정] os.path.join을 사용해 운영체제에 맞는 정확한 전체 경로 생성
        full_path = os.path.join(CLIENT_DIR, path)

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                file_contents[key] = f.read()
                print(f"[OK] {key} 로드 완료")
        except FileNotFoundError:
            print(f"[Warning] 파일을 찾을 수 없습니다: {full_path}")
            file_contents[key] = ""

    # 3. [핵심 최적화] HTML 선조립 (Pre-assembling)
    # 매 요청마다 header+body를 조립하는 비용을 아끼기 위해,
    # 변하지 않는 부분(Index + Header + Body)을 미리 합쳐둡니다.
    # {{footer}} 부분만 구멍을 뚫어놓고 나중에 끼워 넣습니다.
    
    base_html = file_contents['index']
    base_html = base_html.replace('{{header}}', file_contents['header'])
    base_html = base_html.replace('{{body}}', file_contents['body'])
    
    # 조립된 뼈대를 'base_layout'이라는 키로 저장
    TEMPLATE_CACHE['base_layout'] = base_html
    
    # 나머지 개별 부품들도 캐시에 저장 (나중에 꺼내 쓰기 위함)
    for key, content in file_contents.items():
        if key not in ['index', 'header', 'body']: # 이미 조립된 건 제외해도 되지만, 일단 다 넣습니다.
            TEMPLATE_CACHE[key] = content

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # [기존 코드 주석처리] 로그 출력은 유지
        print(f"요청 메서드: {self.command}")
        print(f"요청 경로: {self.path}")
        print(f"요청 헤더: \n{self.headers}")

        path = self.path

        # ------------------------------------------------------------------
        # [삭제됨] 1. 동적 푸터 매핑 테이블 (데이터 중심 설계)
        # 이유: 이제는 '파일 경로'를 매핑하는 게 아니라, 메모리에 있는 '캐시 키'를 매핑해야 합니다.
        # ------------------------------------------------------------------
        # footer_map = {
        #     '/': 'client/page/footer.html',
        #     '/01': 'client/page/bottom/footer01.html',
        #     ...
        # }

        # ------------------------------------------------------------------
        # [삭제됨] 2. 라우팅 로직 처리 & 파일 경로 계산
        # 이유: 파일을 직접 open()하지 않으므로, 파일 경로를 계산할 필요가 없어졌습니다.
        # ------------------------------------------------------------------
        # is_dynamic_route = path in footer_map
        # if is_dynamic_route or path == '/':
        #     file_path = 'client/index.html'
        # else:
        #     file_path = f'client{path}'

        # ------------------------------------------------------------------
        # [변경됨] 3. 확장자 처리 및 응답 생성 로직 분기
        # 이유: HTML은 '메모리 조립'을 해야 하고, CSS는 '메모리 배달'을 해야 하므로 로직을 나눕니다.
        # ------------------------------------------------------------------

        # === [A] CSS 처리 구간 (정적 파일) ===
        if path.endswith('.css'):
            # [수정] 파일 경로 검사 대신 캐시에서 바로 가져옴
            # 현재는 'client/style.css' 하나만 있다고 가정하고 'css_main' 키를 사용합니다.
            # (여러 CSS가 있다면 경로에 따라 키를 다르게 가져오는 로직 필요)
            content = TEMPLATE_CACHE.get('css_main', '')
            
            if content:
                self.send_response(200)
                self.send_header('Content-type', 'text/css; charset=utf-8') # [중요] 브라우저에게 CSS임을 알림
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, "CSS File Not Found in Cache")
            return # CSS 처리가 끝났으면 함수 종료!

        # [삭제됨] JS 처리 로직
        # 이유: 현재 프로젝트 구조상 외부 JS 파일 요청이 없으므로 제거했습니다.
        # elif file_path.endswith('.js'): ...
            
        # === [B] HTML 페이지 처리 구간 (동적 조립) ===
        
        # [추가됨] 경로에 따른 푸터 키 매핑 (파일 경로가 아닌 캐시 키를 매핑)
        footer_mapping_keys = {
            '/': 'footer_default',
            '/01': 'footer_01',
            '/02': 'footer_02',
            '/03': 'footer_03',
            '/04': 'footer_04',
            '/05': 'footer_05',
        }

        # 1. 뼈대 가져오기 (Index + Header + Body가 이미 합쳐진 것)
        # [최적화] open() 함수 제거 -> TEMPLATE_CACHE에서 조회
        content = TEMPLATE_CACHE.get('base_layout', '')

        # 2. 경로에 맞는 푸터 부품 가져오기
        # 매핑에 없는 경로라면 기본 푸터(footer_default)를 사용하거나 404 처리를 할 수 있음
        if path not in footer_mapping_keys and path != '/':
            # [추가] 엉뚱한 경로 요청 시 404 페이지 반환
            error_content = TEMPLATE_CACHE.get('404', '<h1>404 Not Found</h1>')
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(error_content.encode('utf-8'))
            return

        footer_key = footer_mapping_keys.get(path, 'footer_default')
        footer_content = TEMPLATE_CACHE.get(footer_key, '')

        # ------------------------------------------------------------------
        # [삭제됨] 파일 읽기 및 반복 치환 로직
        # 이유: 이미 load_templates()에서 base_layout을 만들었으므로,
        # header, body를 읽고 치환하는 반복 작업이 필요 없습니다.
        # ------------------------------------------------------------------
        # if file_path == 'client/index.html':
        #     with open(file_path, ...) as f: ...
        #     with open('client/page/header.html', ...) as h: ...
        #     content = content.replace('{{header}}', header_content) ...

        # [핵심] 3. 마지막 남은 조각(Footer) 끼우기
        # CPU는 이제 단 한 번의 replace 작업만 수행하면 됩니다.
        content = content.replace('{{footer}}', footer_content)

        # 4. 스크립트 주입 (기존 기능 유지)
        console_script = "<script>console.log('응답을 받았습니다: 서버 메모리에서 조립됨(Fast!)');</script>"
        content = content.replace('</body>', f'{console_script}</body>')

        # 5. 응답 전송
        # [변경] file_path 변수가 사라졌으므로 항상 200 OK로 처리 (404는 위에서 처리함)
        print(f"\n--- [Server Response Out] ---")
        print(f"상태 코드(Status): 200")
        print(f"대상 경로(Path): {path}")
        print(f"컨텐츠 타입(Content-Type): text/html") # HTML 구간이므로 고정
        print(f"-----------------------------\n")
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    # [삭제됨] send_error_page 메서드
    # 이유: 404 에러 처리도 캐시 메모리를 이용하는 방식으로 통합되어 별도 메서드가 불필요해졌습니다.
    # def send_error_page(self, file_path): ...

# 서버 실행부
host = 'localhost'
port = 7777

# [추가됨] 서버 시작 전, 반드시 템플릿 로딩을 먼저 수행합니다!
load_templates()

server = HTTPServer((host, port), MyRequestHandler)

try:
    print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
    print("종료하려면 터미널에서 Ctrl+C를 누르세요.")
    server.serve_forever()
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()
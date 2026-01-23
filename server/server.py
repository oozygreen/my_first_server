from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# 1. HTML 및 CSS 컨텐츠 정의 (파일 대신 변수에 직접 담습니다)
# ==============================================================================

# [CSS] 스타일시트
CSS_CONTENT = """
body { font-family: sans-serif; text-align: center; margin: 0; padding: 0; }
header { background: #f0f0f0; padding: 20px; border-bottom: 1px solid #ccc; }
main { padding: 50px; min-height: 200px; }
footer { background: #333; color: white; padding: 20px; position: fixed; bottom: 0; width: 100%; }
.footer-nav a { color: white; margin: 0 10px; text-decoration: none; }
"""

# [HTML] 조각들 (Components)
HTML_HEADER = """
<header>
    <h1>My Python Server (In-Memory)</h1>
    <nav>
        <a href="/">HOME</a> | 
        <a href="/01">Page 1</a> | 
        <a href="/02">Page 2</a> | 
        <a href="/03">Page 3</a>
    </nav>
</header>
"""

HTML_BODY = """
<main>
    <h2>본문 영역입니다</h2>
    <p>서버 메모리 변수에서 직접 로딩된 컨텐츠입니다.</p>
    <p>더 이상 파일 경로 때문에 고통받지 않아요! 😄</p>
</main>
"""

# 기본 인덱스 껍데기 (템플릿)
HTML_INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Lv.3 Server</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    {{header}}
    {{body}}
    {{footer}}
</body>
</html>
"""

# [HTML] 푸터 모음 (Footers)
HTML_FOOTER_DEFAULT = """
<footer>
    <p>기본 푸터입니다.</p>
</footer>
"""

HTML_FOOTER_01 = """
<footer style="background: navy;">
    <p>1번 페이지 전용 푸터 (Navy)</p>
</footer>
"""

HTML_FOOTER_02 = """
<footer style="background: darkgreen;">
    <p>2번 페이지 전용 푸터 (Green)</p>
</footer>
"""

HTML_FOOTER_03 = """
<footer style="background: darkred;">
    <p>3번 페이지 전용 푸터 (Red)</p>
</footer>
"""

# 404 페이지
HTML_404 = """
<!DOCTYPE html>
<html>
<body>
    <h1 style="color:red">404 Not Found</h1>
    <p>요청하신 페이지를 찾을 수 없습니다.</p>
</body>
</html>
"""

# ==============================================================================
# 2. 템플릿 조립 및 캐싱 로직
# ==============================================================================

TEMPLATE_CACHE = {}
FOOTER_MAP = {
    '/': HTML_FOOTER_DEFAULT,
    '/01': HTML_FOOTER_01,
    '/02': HTML_FOOTER_02,
    '/03': HTML_FOOTER_03,
}

def init_templates():
    print("--- [System] 메모리 변수에서 템플릿을 조립합니다 ---")
    
    # 1. 기본 뼈대(Base Layout) 조립: Index + Header + Body
    # (Footer는 요청마다 갈아끼우기 위해 {{footer}}로 남겨둡니다)
    base = HTML_INDEX_TEMPLATE
    base = base.replace('{{header}}', HTML_HEADER)
    base = base.replace('{{body}}', HTML_BODY)
    
    TEMPLATE_CACHE['base_layout'] = base
    
    # 2. CSS 및 404도 캐시에 등록
    TEMPLATE_CACHE['css'] = CSS_CONTENT
    TEMPLATE_CACHE['404'] = HTML_404
    
    print("[OK] 조립 완료! 파일을 읽지 않고 변수를 사용했습니다.")

# ==============================================================================
# 3. 요청 핸들러 (서버 로직)
# ==============================================================================

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # --- [A] CSS 처리 ---
        if path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css; charset=utf-8')
            self.end_headers()
            self.wfile.write(TEMPLATE_CACHE['css'].encode('utf-8'))
            return

        # --- [B] HTML 페이지 처리 ---
        
        # 1. 조립된 기본 뼈대 가져오기
        content = TEMPLATE_CACHE.get('base_layout')
        
        # 2. 경로에 맞는 푸터 선택 (없으면 404)
        if path in FOOTER_MAP:
            footer_content = FOOTER_MAP[path]
        else:
            # 엉뚱한 경로면 404 페이지 응답
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(TEMPLATE_CACHE['404'].encode('utf-8'))
            return

        # 3. 최종 조립: 뼈대에 푸터 끼우기
        final_content = content.replace('{{footer}}', footer_content)
        
        # 4. 응답 전송
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(final_content.encode('utf-8'))
        
        # 로그 출력
        print(f"[Request] {path} -> 200 OK (Footer changed)")

# ==============================================================================
# 4. 서버 실행
# ==============================================================================

host = 'localhost'
port = 7777

# 서버 시작 전 조립 실행
init_templates()

server = HTTPServer((host, port), MyRequestHandler)

try:
    print(f"\n🚀 서버가 시작되었습니다. http://{host}:{port}")
    print("경로 문제 없는 All-in-One 서버입니다. Ctrl+C로 종료하세요.\n")
    server.serve_forever()
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()
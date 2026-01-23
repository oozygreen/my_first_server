from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# 1. HTML 및 CSS 컨텐츠 정의 (파일 대신 변수에 직접 담습니다)
# ==============================================================================

# [CSS] 스타일시트
CSS_CONTENT = """
* { margin: 0; padding: 0; box-sizing: border-box; }

/* Header */
header { width: 100%; height: 60px; background-color: #36c; display: flex; align-items: center; justify-content: space-between; padding: 0 20px; }
header a { color: white; text-decoration: none; display: block; padding: 10px; }
header h1 { color: white; font-size: 30px; }
header nav ul { list-style: none; display: flex; gap: 0px; }
header nav ul li button { background-color: transparent; color: white; font-weight: bold; border: none; font-size: 16px; position: relative; }
header nav ul li button::after { content: ''; display: block; width: 0; height: 2px; background-color: white; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%); transition: width 0.3s; }
header nav ul li button:hover::after { width: 100%; }

/* Body */
.maslow-needs { min-height: calc(100vh - 60px - 160px); display: flex; align-items: center; justify-content: center; padding: 40px 0; }
.pyramid { list-style: none; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.pyramid > li { height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.needs-title { font-weight: bold; font-size: 20px; margin-bottom: 10px; }
.self-actualization { width: 160px; height: 120px; background-color: transparent; position: relative; }
.self-actualization::before { z-index: -1; display: block; content: ''; box-sizing: border-box; width: 160px; height: 120px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: transparent; border-left: 80px solid transparent; border-right: 80px solid transparent; border-bottom: 120px solid #DFF5EA; }
.esteem { width: 320px; height: 120px; background-color: transparent; position: relative; }
.esteem::before { z-index: -1; display: block; content: ''; box-sizing: border-box; width: 320px; height: 120px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: transparent; border-left: 80px solid transparent; border-right: 80px solid transparent; border-bottom: 120px solid #BFE6D3; }
.love_belonging { width: 480px; height: 120px; background-color: transparent; position: relative; }
.love_belonging::before { z-index: -1; display: block; content: ''; box-sizing: border-box; width: 480px; height: 120px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: transparent; border-left: 80px solid transparent; border-right: 80px solid transparent; border-bottom: 120px solid #9ED9D5; }
.safety { width: 640px; height: 120px; background-color: transparent; position: relative; }
.safety::before { z-index: -1; display: block; content: ''; box-sizing: border-box; width: 640px; height: 120px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: transparent; border-left: 80px solid transparent; border-right: 80px solid transparent; border-bottom: 120px solid #7FC9D9; }
.physiological { width: 800px; height: 120px; background-color: transparent; position: relative; }
.physiological::before { z-index: -1; display: block; content: ''; box-sizing: border-box; width: 800px; height: 120px; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: transparent; border-left: 80px solid transparent; border-right: 80px solid transparent; border-bottom: 120px solid #A7CFEA; }

/* Footer */
footer { width: 100%; height: 160px; padding: 30px; background: #333; color: white; }
footer .footer-title { font-size: 24px; font-weight: bold; margin-bottom: 10px; }
footer .footer-content { font-size: 16px; line-height: 1.5; }
"""

# [HTML] 조각들 (Components)
HTML_HEADER = """
<header>
    <h1><a href="/">매슬로우의 욕구이론</a></h1>
    <nav>
        <ul>
            <li>
                <button><a href="/01">생리적 욕구</a></button>
            </li>
            <li>
                <button><a href="/02">안전 욕구</a></button>
            </li>
            <li>
                <button><a href="/03">소속과 사랑의 욕구</a></button>
            </li>
            <li>
                <button><a href="/04">존경의 욕구</a></button>
            </li>
            <li>
                <button><a href="/05">자아실현의 욕구</a></button>
            </li>
        </ul>
    </nav>
</header>
"""

HTML_BODY = """
<main class="maslow-needs">
    <ul class="pyramid">
        <li class="self-actualization">
            <div>
                <p class="needs-title">자아 실현의 욕구</p>
                <p class="needs-content">자신의 잠재력을 최대한<br>개발하고자 하는 욕구</p>
            </div>
        </li>
        <li class="esteem">
            <div>
                <p class="needs-title">존경의 욕구</p>
                <p class="needs-content">자존감, 성취, 유능함, 자아존중 및<br>타인에게 인정받고 존중받고자 하는 욕구</p>
            </div>
        </li>
        <li class="love_belonging">
            <div>
                <p class="needs-title">소속과 사랑의 욕구</p>
                <p class="needs-content">다른 사람들로부터 인정을 받고 사랑받기를 원하며<br>집단에 소속하기를 바라는 욕구</p>
            </div>
        </li>
        <li class="safety">
            <div>
                <p class="needs-title">안전 욕구</p>
                <p class="needs-content">안전감과 안정의 욕구이며 위험과<br>공포 사고, 박탈 등으로 안전하고자 하는 욕구</p>
            </div>
        </li>
        <li class="physiological">
            <div>
                <p class="needs-title">생리적 욕구</p>
                <p class="needs-content">인간의 의식주와 관련된 생명을 유지하는 욕구,<br>배고픔과 갈증을 해소하려는 욕구</p>
            </div>
        </li>
    </ul>
</main>
"""

# 기본 인덱스 껍데기 (템플릿)
HTML_INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>매슬로우의 욕구이론</title>

    <link rel="stylesheet" href="./css/style.css">
</head>
<body>
    <!-- header.html 영역 -->
    {{header}}
    
    <!-- body.html 영역 -->
    {{body}}
    
    <!-- footer.html 영역 -->
    {{footer}}
</body>
</html>
"""

# [HTML] 푸터 모음 (Footers)
HTML_FOOTER_DEFAULT = """
<footer>
    <p class="footer-title">어떤 욕구가 궁금하세요?</p>
    <p class="footer-content">헤더의 욕구 버튼을 클릭하면 해당 욕구에 대한 설명이 나타납니다.</p>
</footer>
"""

HTML_FOOTER_01 = """
<footer>
    <p class="footer-title">생리적 욕구</p>
    <p class="footer-content">인간의 의식주와 관련된 생명을 유지하는 욕구, 배고픔과 갈증을 해소하려는 욕구</p>
</footer>
"""

HTML_FOOTER_02 = """
<footer>
    <p class="footer-title">안전 욕구</p>
    <p class="footer-content">안전감과 안정의 욕구이며 위험과 공포 사고, 박탈 등으로 안전하고자 하는 욕구</p>
</footer>
"""

HTML_FOOTER_03 = """
<footer>
    <p class="footer-title">소속과 사랑의 욕구</p>
    <p class="footer-content">다른 사람들로부터 인정을 받고 사랑받기를 원하며 집단에 소속하기를 바라는 욕구</p>
</footer>
"""

HTML_FOOTER_04 = """
<footer>
    <p class="footer-title">존경의 욕구</p>
    <p class="footer-content">자존감, 성취, 유능함, 자아존중 및 타인에게 인정받고 존중받고자 하는 욕구</p>
</footer>
"""

HTML_FOOTER_05 = """
<footer>
    <p class="footer-title">자아 실현의 욕구</p>
    <p class="footer-content">자신의 잠재력을 최대한 개발하고자 하는 욕구</p>
</footer>
"""

# 404 페이지
HTML_404 = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 Error</title>
</head>
<body>
    <h1>404에러 어서오고 ㅋㅋㅋㅋ</h1>
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
    '/04': HTML_FOOTER_04,
    '/05': HTML_FOOTER_05,
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
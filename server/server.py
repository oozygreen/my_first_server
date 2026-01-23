from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# 1. HTML 및 CSS 컨텐츠 정의 (파일 대신 변수에 직접 담습니다)
# ==============================================================================

class make_tag:
    def __init__(self, tag_name, content="", href=None, class_=None, style=None, **others):
        self.tag_name = tag_name
        self.content = content
        
        # 속성 정리
        self.final_attrs = others
        if href: self.final_attrs['href'] = href
        if class_: self.final_attrs['class'] = class_
        if style:
            if isinstance(style, dict):
                self.final_attrs['style'] = "; ".join([f"{k}: {v}" for k, v in style.items()])
            else:
                self.final_attrs['style'] = style

    def render(self):
        # 속성 문자열 생성
        attr_str = ""
        for key, value in self.final_attrs.items():
            attr_str += f' {key}="{value}"'

        # 내용물(Content) 렌더링 로직 (재귀)
        real_content = ""
        
        if isinstance(self.content, make_tag):
            real_content = self.content.render()
        elif isinstance(self.content, list): # 리스트가 들어오면 하나씩 풀어서 렌더링
            for item in self.content:
                if isinstance(item, make_tag):
                    real_content += item.render()
                else:
                    real_content += str(item)
        else:
            real_content = str(self.content)

        return f"<{self.tag_name}{attr_str}>{real_content}</{self.tag_name}>"




# 헤더 생성
HEADER = make_tag(
    "header",
    style="width: 100%; height: 60px; background-color: #36c; display: flex; align-items: center; justify-content: space-between; padding: 0 20px;",
    content=[
        # 1. 로고
        make_tag(
            "h1",
            style="color: white; font-size: 30px;",
            content=make_tag(
                "a",
                stlye="color: white; text-decoration: none; display: block; padding: 10px;",
                href="/",
                content="매슬로우의 욕구이론"
            )
        ),

        # 2. 메뉴
        make_tag(
            "nav",
            content=make_tag(
                "ul",
                style="list-style: none; display: flex; gap: 0px;",
                content=[
                    make_tag(
                        "li", 
                        content=make_tag(
                            "button", 
                            style="background-color: transparent; color: white; font-weight: bold; border: none; font-size: 16px; position: relative;",
                            content=make_tag(
                                "a", 
                                style="color: white; text-decoration: none; display: block; padding: 10px;",
                                href=item["href"],
                                content=item["text"]
                            ) 
                        )
                    ) for item in [
                        {"href": "/01", "text": "생리적 욕구"},
                        {"href": "/02", "text": "안전 욕구"},
                        {"href": "/03", "text": "소속과 사랑의 욕구"},
                        {"href": "/04", "text": "존경의 욕구"},
                        {"href": "/05", "text": "자아실현의 욕구"}
                    ]
                ]
            )
        )
    ]
)

MAIN = make_tag(
    "main",
    class_="maslow-needs",
    # 전체 레이아웃 잡는 스타일 (인라인)
    style="min-height: calc(100vh - 60px - 160px); display: flex; align-items: center; justify-content: center; padding: 40px 0;",
    content=make_tag(
        "ul",
        class_="pyramid",
        # 리스트 스타일 제거 및 정렬 (인라인)
        style="list-style: none; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 0; margin: 0;",
        content=[
            make_tag(
                "li",
                # [중요] 가상요소(도형)를 그리기 위한 클래스명 연결
                class_=item["class"], 
                # 개별 층의 높이와 텍스트 정렬 (인라인)
                style="height: 120px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; position: relative;", 
                content=make_tag(
                    "div",
                    content=[
                        # 제목
                        make_tag(
                            "p",
                            class_="needs-title",
                            style="font-weight: bold; font-size: 20px; margin-bottom: 10px; margin-top: 0;",
                            content=item["title"]
                        ),
                        # 설명
                        make_tag(
                            "p",
                            class_="needs-content",
                            style="margin: 0; line-height: 1.5;",
                            content=item["desc"]
                        )
                    ]
                )
            ) for item in [
                # 위에서부터 아래로 내려가는 순서 (데이터 리스트)
                {
                    "class": "self-actualization", 
                    "title": "자아 실현의 욕구", 
                    "desc": "자신의 잠재력을 최대한<br>개발하고자 하는 욕구"
                },
                {
                    "class": "esteem", 
                    "title": "존경의 욕구", 
                    "desc": "자존감, 성취, 유능함, 자아존중 및<br>타인에게 인정받고 존중받고자 하는 욕구"
                },
                {
                    "class": "love_belonging", 
                    "title": "소속과 사랑의 욕구", 
                    "desc": "다른 사람들로부터 인정을 받고 사랑받기를 원하며<br>집단에 소속하기를 바라는 욕구"
                },
                {
                    "class": "safety", 
                    "title": "안전 욕구", 
                    "desc": "안전감과 안정의 욕구이며 위험과<br>공포 사고, 박탈 등으로 안전하고자 하는 욕구"
                },
                {
                    "class": "physiological", 
                    "title": "생리적 욕구", 
                    "desc": "인간의 의식주와 관련된 생명을 유지하는 욕구,<br>배고픔과 갈증을 해소하려는 욕구"
                }
            ]
        ]
    )
)



# 기본 인덱스 껍데기 (템플릿)
HTML_INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>매슬로우의 욕구이론</title>
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
    base = base.replace('{{header}}', HEADER)
    base = base.replace('{{body}}', MAIN)
    
    TEMPLATE_CACHE['base_layout'] = base
    
    # 2. CSS 및 404도 캐시에 등록
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
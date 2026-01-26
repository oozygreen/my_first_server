from http.server import HTTPServer, BaseHTTPRequestHandler

# ==============================================================================
# [SECTION 1] HTML 생성 도구 (Tool)
# ==============================================================================

class make_tag:
    """
    HTML 태그를 객체 형태로 생성하고 렌더링하는 클래스
    """
    def __init__(self, tag_name, content="", href=None, class_=None, style=None, **others):
        self.tag_name = tag_name
        self.content = content
        
        # 속성 정리
        self.final_attrs = others
        if href: self.final_attrs['href'] = href
        if class_: self.final_attrs['class'] = class_
        
        # 스타일 처리 (딕셔너리 or 문자열)
        if style:
            if isinstance(style, dict):
                self.final_attrs['style'] = "; ".join([f"{k}: {v}" for k, v in style.items()])
            else:
                self.final_attrs['style'] = style

    def render(self):
        """객체를 HTML 문자열로 변환"""
        # 1. 속성 문자열 생성
        attr_str = ""
        for key, value in self.final_attrs.items():
            attr_str += f' {key}="{value}"'

        # 2. 내용물(Content) 렌더링 (재귀 처리)
        real_content = ""
        
        if isinstance(self.content, make_tag):
            real_content = self.content.render()
        elif isinstance(self.content, list): 
            for item in self.content:
                if isinstance(item, make_tag):
                    real_content += item.render()
                else:
                    real_content += str(item)
        else:
            real_content = str(self.content)

        return f"<{self.tag_name}{attr_str}>{real_content}</{self.tag_name}>"


# ==============================================================================
# [SECTION 2] 스타일 및 컨텐츠 데이터 (Data & CSS)
# ==============================================================================

# 1. CSS 스타일
CSS_STYLES = """
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

# 2. Footer 데이터 정의
FOOTER_DATA = {
    '/': {
        "title": "어떤 욕구가 궁금하세요?", 
        "desc": "헤더의 욕구 버튼을 클릭하면 해당 욕구에 대한 설명이 나타납니다."
    },
    '/01': {
        "title": "생리적 욕구", 
        "desc": "인간의 의식주와 관련된 생명을 유지하는 욕구, 배고픔과 갈증을 해소하려는 욕구"
    },
    '/02': {
        "title": "안전 욕구", 
        "desc": "안전감과 안정의 욕구이며 위험과 공포 사고, 박탈 등으로 안전하고자 하는 욕구"
    },
    '/03': {
        "title": "소속과 사랑의 욕구", 
        "desc": "다른 사람들로부터 인정을 받고 사랑받기를 원하며 집단에 소속하기를 바라는 욕구"
    },
    '/04': {
        "title": "존경의 욕구", 
        "desc": "자존감, 성취, 유능함, 자아존중 및 타인에게 인정받고 존중받고자 하는 욕구"
    },
    '/05': {
        "title": "자아 실현의 욕구", 
        "desc": "자신의 잠재력을 최대한 개발하고자 하는 욕구"
    }
}


# ==============================================================================
# [SECTION 3] HTML 구조 조립 (Components)
# ==============================================================================

# 1. 헤더 (Header)
HEADER = make_tag(
    "header",
    content=[
        # 로고
        make_tag("h1", content=make_tag("a", href="/", content="매슬로우의 욕구이론")),
        # 네비게이션
        make_tag(
            "nav",
            content=make_tag(
                "ul",
                content=[
                    make_tag(
                        "li", 
                        content=make_tag(
                            "button", 
                            content=make_tag("a", href=item["href"], content=item["text"]) 
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

# 2. 메인 (Main Body)
MAIN = make_tag(
    "main",
    class_="maslow-needs",
    content=make_tag(
        "ul",
        class_="pyramid",
        content=[
            make_tag(
                "li",
                class_=item["class"], 
                content=make_tag(
                    "div",
                    content=[
                        make_tag("p", class_="needs-title", content=item["title"]),
                        make_tag("p", class_="needs-content", content=item["desc"])
                    ]
                )
            ) for item in [
                {"class": "self-actualization", "title": "자아 실현의 욕구", "desc": "자신의 잠재력을 최대한<br>개발하고자 하는 욕구"},
                {"class": "esteem", "title": "존경의 욕구", "desc": "자존감, 성취, 유능함, 자아존중 및<br>타인에게 인정받고 존중받고자 하는 욕구"},
                {"class": "love_belonging", "title": "소속과 사랑의 욕구", "desc": "다른 사람들로부터 인정을 받고 사랑받기를 원하며<br>집단에 소속하기를 바라는 욕구"},
                {"class": "safety", "title": "안전 욕구", "desc": "안전감과 안정의 욕구이며 위험과<br>공포 사고, 박탈 등으로 안전하고자 하는 욕구"},
                {"class": "physiological", "title": "생리적 욕구", "desc": "인간의 의식주와 관련된 생명을 유지하는 욕구,<br>배고픔과 갈증을 해소하려는 욕구"}
            ]
        ]
    )
)

# 3. 푸터 생성 헬퍼 함수
def create_footer(title, desc):
    return make_tag(
        "footer",
        content=[
            make_tag("p", class_="footer-title", content=title),
            make_tag("p", class_="footer-content", content=desc)
        ]
    )


# ==============================================================================
# [SECTION 4] 템플릿 관리 및 초기화 (Templates)
# ==============================================================================

HTML_INDEX_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>매슬로우의 욕구이론</title>
    <style>{{css}}</style>
</head>
<body>
    {{header}}
    {{body}}
    {{footer}}
</body>
</html>
"""

HTML_404 = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>404 Error</title>
</head>
<body>
    <h1>404에러 어서오고 ㅋㅋㅋㅋ</h1>
</body>
</html>
"""

TEMPLATE_CACHE = {}
FOOTER_MAP = {}

def init_templates():
    print("--- [System] 템플릿 조립을 시작합니다 ---")
    
    # 1. Footer Map 미리 생성 (효율성)
    for path, data in FOOTER_DATA.items():
        footer_obj = create_footer(data['title'], data['desc'])
        FOOTER_MAP[path] = footer_obj.render()
    
    # 2. 기본 레이아웃 조립 (Header, Main, CSS 주입)
    base = HTML_INDEX_TEMPLATE
    base = base.replace('{{css}}', CSS_STYLES)
    base = base.replace('{{header}}', HEADER.render()) 
    base = base.replace('{{body}}', MAIN.render())
    
    TEMPLATE_CACHE['base_layout'] = base
    TEMPLATE_CACHE['404'] = HTML_404
    
    print("[System] 조립 완료! (Base Layout + 6 Footers ready)")


# ==============================================================================
# [SECTION 5] 서버 핸들러 (Server Logic)
# ==============================================================================

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        
        # 1. 기본 레이아웃 가져오기
        content = TEMPLATE_CACHE.get('base_layout')
        
        # 2. 요청 경로에 맞는 푸터 선택
        if path in FOOTER_MAP:
            footer_content = FOOTER_MAP[path]
            status_code = 200
        else:
            # 경로가 없으면 404 페이지 리턴
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(TEMPLATE_CACHE['404'].encode('utf-8'))
            return

        # 3. 최종 조립: 레이아웃에 푸터 끼우기
        final_content = content.replace('{{footer}}', footer_content)
        
        # 4. 응답 전송
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(final_content.encode('utf-8'))
        
        print(f"[Request] {path} -> 200 OK")


# ==============================================================================
# [SECTION 6] 메인 실행 (Execution)
# ==============================================================================

if __name__ == "__main__":
    host = 'localhost'
    port = 7777

    # 서버 시작 전 템플릿 조립
    init_templates()

    server = HTTPServer((host, port), MyRequestHandler)

    try:
        print(f"\n🚀 서버가 시작되었습니다. http://{host}:{port}")
        print("Ctrl+C로 종료할 수 있습니다.\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
        server.server_close()
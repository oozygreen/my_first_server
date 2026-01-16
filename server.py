from http.server import HTTPServer, BaseHTTPRequestHandler
# http.server는 무엇이길래 from으로 불러오는 걸까?
# 그 안에서 HTTPServer와 BaseHTTPRequestHandler라는 무언가를 따로 꺼내온 것 같은데
# 이 코드가 나중에 어떻게 필요하길래 가장 위에서 선언해준 걸까?
# 일반적으로 import os 등의 코드는 자주 봤었는데 정확하게 어디서 불러오고 어떻게 동작하는걸까?
# HTTP가 뭔지, 서버가 뭔지, 핸들러가 뭔지, 베이스가 뭔지 등등을 알아봐야 할 것 같다.

class MyRequestHandler(BaseHTTPRequestHandler):
# 클래스다. 한번 정리해봤으니 이 정도는 겁나지 않지.
# MtRequestHandler라는 이름의 클래스를 정의하고 매개변수로 BaseHTTPRequestHandler를 받는 형태구나.
# BaseHTTPRequestHandler는 바로 위에서 import했던 건데 여기서 또 사용되네?
    
    def do_GET(self):
    # 메서드군. do_GET이라는 이름으로 정의하는데 do_POST는 보이지 않는다.
    # 지금은 서버에서 일방적으로 전송만 하는 형태라서 POST가 필요 없다고 생각되는데
    # 나중에 클라이언트에서 데이터를 보내는 형태가 되면 POST도 구현해야 할까?
        self.send_response(200)
        # send_response 메서드를 호출하는데 200이라는 숫자를 매개변수로 전달받는다.
        # send_response 메서드는 어느 클래스에서 정의된 메서드지?
        # BaseHTTPRequestHandler 클래스에서 정의된 메서드일까?
        # ----------------------------------
        # 200은 성공을 나타내는 것 같은데
        # 403, 404, 500 등도 있다고 알고 있는데 이 숫자들은 어디서 정해진 걸까?
        # 각 숫자들이 의미하는 바를 알아봐야 할 것 같다.

        self.send_header('Content-type', 'text/html; charset=utf-8')
        # send_header 메서드를 호출하는데 'Content-type'과 'text/html; charset=utf-8'이라는 두 개의 매개변수를 전달받는다.
        # send_header 메서드는 어느 클래스에서 정의된 메서드지? 정확히 어떤 역할을 하는 걸까? 왜 header라는 단어가 쓰인 걸까?
        # Content-type은 무엇을 의미하는 걸까?
        # text/html; charset=utf-8은 무슨 뜻이지?
        
        self.end_headers()
        # end_headers 메서드를 호출한다.
        # end_headers 메서드도 어느 클래스에서 정의된 메서드인지, 그리고 왜 이 메서드는 매개변수를 받지 않는지 알아보자
        
        message = "<h1>안녕하세요! 파이썬 서버입니다.</h1>"
        # 기본적인 변수에 html 코드를 담아놓은 상태네
        self.wfile.write(message.encode('utf-8'))
        # wfile은 뭐지? self.뒤에 함수나 메서드같은게 붙을텐데 이건 글자 색깔이 다르네?
        # write 메서드를 호출하는데 딱 봐도 쓰는 것 같아 보이지만 어디서 온 메서드인지, 혹은 파이썬 내장함수인지 짚어보자
        # message 변수를 utf-8형태로 인코딩해서 전달하는 것 같은데 encode 메서드는 어디서 온 메서드지? 파이썬 내장함수인가?

host = 'localhost'
port = 8000
# localhost 대신 127.0.0.1을 써도 되겠지? 다른 대역을 지정하면 왜 안될까? localhost대신 kjhost라고 쓰면 왜 안될까?
# 그러면 이 ip를 외부 ip로 바꾸면 어떻게 되지? 혹은 외부에서 접근 가능하게 공개하려면 어떻게 해야 하지?
# port는 8000말고 8080쓰기도 하고 3000쓰기도 하던데 의미는 없다고 들었지만 그럼 7777같은거 써도 되나?
# 사람들이 이 숫자로 멋도 부릴법 한데 왜 맨날 정해진 8000,8080,3000만 쓰지?

server = HTTPServer((host, port), MyRequestHandler)
# 떴다. HTTPServer 클래스다 아까 위에서 본거. 그럼 이게 서버를 구동시키는 클래스같은거였나 보네
# 근데 안에서 매개변수로 받은 MyRequestHandler는 뭐지? 아까 정의한 클래스인데?
# 어떻게 된거야? 핸들러를 내가 따로 만들어야 할 필요가 있어? 핸들러가 뭐길래?
# 별거 아닌 코드 같아 보이는데 왜 내가 따로 커스텀해서 구동해야 되는거지?

print(f"서버가 시작되었습니다. http://{host}:{port} 로 접속해보세요.")
print("종료하려면 터미널에서 Ctrl+C를 누르세요.")

try:
    server.serve_forever()
    # serve_forever 메서드는 HTTPServer 클래스에서 정의된 메서드겠지?
    # 느낌 상 의도적으로 중단시키지 않으면 계속 서버를 구동하고 있어라 라는 의미 인거같은데 맞나?
except KeyboardInterrupt:
    print("\n서버를 종료합니다.")
    server.server_close()
    # 마찬가지네. 서버 닫으라는 소리네.
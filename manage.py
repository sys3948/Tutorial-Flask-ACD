# 파일 실행하는 스크립트 파일.


from app import create_app

app = create_app('default')

if __name__ == '__main__':
    app.run()
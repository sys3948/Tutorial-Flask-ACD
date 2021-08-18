from flask import render_template
from . import main

# application fectory 및 blueprint를 사용할 시 에러 핸들러는 다음과 같이 구현한다.

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@main.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

'''
비교연사자

   ==
   !=
   <
   >
   <=, >=

and, or, not 연산자.

    and : A and B ==> A:True, B:True == True
    or : A or B ==> (A:True, B:True),(A:True, B:False),(A:False, B:True) == True
    not : not A,  True ==> False, False ==> True, 0 not in [1, 2, 3, 4] ==> True

in 연산자

pass : 아무것도 실행하지 않는다.


if, else if, else

i = 100

if i < 0:
    print("i는 0보다 작은 수입니다!")
elif i > 50:
    print("i는 50보다 큰 수입니다.")
else:
    print("문제가 발생했습니다.")


-------------------------------------------------------------------------------

while (반복문)

while(반복 조건문){
    실행문
}

while 반복 조건문 :
    실행문

----------------------------------------------------------------------------------

for(int i = 0; i < 조건문; i++){ <-- C or Java etc..
    실행문
}

python for statement

for i in range():
    실행문

i == 변수
range() : 연속된 값이 있는 데이터.(문자열, 리스트, 튜플, 셋, 닥셔너리 -- keys(), value(), items())



__init__ == __init__.py가 속해있는 폴더 이름으로 불러올 수 있다.

------------------------------------------------
연습 문제 풀이.
for i in range(5):
    print(i + 1)

num = 0
while num < 5:
    num += 1
    print(num)
print('for statement print!')
for j in range(2):
    for i in range(5):
        print(i + 1)


print('='*100)
print('while statement print!')


up_num = 0
while up_num < 2:
    num = 0
    while num < 5:
        num += 1
        print(num)
    up_num += 1


print('for statement print!')
for j in range(2):
    for i in range(5):
        print(i + 1, end = " ")
    print()

print('='*100)
print('while statement print!')
up_num = 0
while up_num < 2:
    num = 0
    while num < 5:
        num += 1
        print(num, end = " ")
    print()
    up_num += 1


print('for statement print!')
j = 5
for i in range(5):
    for num in range(j):
        print(num + 1, end=" ")
    print()
    j -= 1


print('='*100)
print('while statement print!')
i = 0
while i < 5:
    j = 0
    while j < 5 - i:
        j += 1 
        print(j, end=" ")
    print()
    i += 1


print('for statement print!')
for i in range(5):
    for num in range(5):
        if num > i-1 :
            print(num + 1, end=" ")
        else:
            print(" ", end=" ")
    print()


print('='*100)
print('while statement print!')
i = 0
while i < 5:
    j = 0
    i += 1
    while j < 5:
        j += 1 
        if j > i-1:
            print(j, end=" ")
        else:
            print(" ", end=" ")
    print()



------------------------------------------------------------------------------------------------
함수.(function)

c
function_type function_name(){
  funtion_type : int, char, float, void
  return value
}

java
[static, public, etc...] function_type function_name(){
  funtion_type : int, char, float, void
  return value
}

python
def function_name():
    실행 내용
    ...
    return value


return : 반환한다라는 뜻

함수에서 return 값 존재하지 않으면 외부에서 함수를 호출할 때 함수에서 처리된 값을 받지 못 함.


매개변수(Parameter), 인자(argument)
def add(a, b): # a, b ==> 매개변수
    return a + b

add(1, 5) # 1, 5 ==> 인자


def add(a, b):
    a + b
    return a + b

def test():
    a = 10
    b = 5
    return a * b

def no_return(a, b):
    c = a+b
    d = a*b
    print(c)
    print(d)

def no_return_and_no_input():
    print('Hello!')

def a_func(*args):
    print(args)

def k_func(**kwargs):
    print(kwargs)

def say_myself(name, old, man=True):
    print("나의 이름은 %s다." %(name))
    print("나이는 %d입니다." %(old))
    if man:
        print('저는 남자입니다.')
    else:
        print('저는 여자입니다.')

def test_fun(a):
    a = a + 1

# print(add(1, 5))
# result = test()
# print(result)
# no_return(5, 6)
# print(no_return(5, 6))
# no_return_and_no_input()
# a_func(1, 2,3, 5, 6, 'hello')
# k_func(a=1, b=10, test='test')
# say_myself('지은', 10, man=False)
a = 1
test_fun(a)
print(a)







from / import


import 외부의 .py(파이썬 파일)에 정의된 변수 or 함수 or 클래스를 가져오게 하는 명령어.
import 파일이름(.py는 제외)

import app.email.send_email -- 1
from app.email import send_email -- 2

1
app.email.send_email()
2
send_email()
'''



class User(db.Model):
    __tablename__ == 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)

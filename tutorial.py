비교연사자.

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
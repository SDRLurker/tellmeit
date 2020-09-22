# TellMeIt

## 소개

네이버의 실시간 검색어를 크롤링하여

텔레그램 봇에 등록된 키워드가 검색되면(있다면)

해당 키워드에 대해 알람메세지를 보냅니다.

### 홈페이지 

* https://sdrlurker.github.io/tellmeit/
* https://psbbbot.herokuapp.com/tellmeit/

### 텔레그램 아이디
* [tellmeit_bot](https://telegram.me/tellmeit_bot)

## 사용법

* /알람 키워드1 키워드2 ...

키워드1, 키워드2 (OR 조건) 등을 알람 메세지를 받을 수 있도록 등록합니다.

* /알람

등록된 키워드를 삭제합니다.

* /도움

도움말을 확인합니다.

## 제작동기

2017년 4월 중순부터 2호선을 타고 출근하기 시작하였습니다.

2017년 7월 현재까지 2번 지하철이 고장이 나서 지각을 하였습니다.

지하철 2호선이 고장나면 네이버 실시간 검색어에 올라오게 됩니다.

인터넷 서핑없이 지하철 고장을 미리 현상을 알기 위해 이 봇을 만들었습니다.

## 의존성 관리

```shell
tellmeit$ pip install -r requirements.txt
```

## 프로그램 실행

```shell
tellmeit$ ./tellmeit.sh &
```

## 공지사항 전송하기 예시

```shell
tellmeit$ vi notice.txt # 공지할 내용 작성.
tellmeit$ ./notice.py notice.txt
```

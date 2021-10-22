# [위코드 x 원티드] 백엔드 프리온보딩 선발 과제

## 과제 안내
1. 글 작성, 글 확인, 글 목록 확인, 글 수정, 글 삭제가 되는 API
    - Delete과 Update는 해당 유저의 글만 가능
    - 즉, 유저 생성, 인가, 인증 기능도 필요
    - Read는 pagination 구현 필수
2. 데이터베이스는 in-memory database로 구현
    - 리뷰어가 Database를 따로 설치할 필요 없이 실행하고 확인할 수 있어야 합니다.
    - 예) sqlite3
3. Unit Test 구현시 가산점이 있습니다.

## 과제 정보
### Postman(API)

[https://www.postman.com/wecode-21-1st-kaka0/workspace/wecode-wanted/request/16042359-a21e8222-1453-4531-a032-6089628d2d6f](https://www.postman.com/wecode-21-1st-kaka0/workspace/wecode-wanted/request/16042359-a21e8222-1453-4531-a032-6089628d2d6f)

### Modeling
<img width="1200" alt="스크린샷 2021-10-22 오전 10 21 44" src="https://user-images.githubusercontent.com/8219812/138384135-933f6683-2429-4609-ae6d-10ef008a2656.png">


### 사용한 Framework
- Django(DRF)

### 구현한 방법
- 모델링은 게시판 글을 저장하는 Posts와 회원 정보를 저장하는 Accounts 총 2개의 table로 구성되어 있습니다. 또한 글을 쓴 사람을 알 수 있도록 Posts table에 author이라는 필드를 둬서 Accounts table과 연결하였습니다.
- 로직은 DRF의 ModelViewSet을 사용해서 구현하였습니다.
- 권한은 다음과 같은 조건을 생각해서 DRF에서 제공하고 있는 Permission Class 구현하였습니다.
    - 조회시에는 인증을 하지 않아도 조회되도록 하였습니다.
    - 글 작성시에서는(POST) 인증이 되었을때만 쓸 수 있도록 하였습니다.
    - 글 내용 변경(PATCH)및 삭제(DELETE)는 인증과 해당글을 작성한 사용자만 할 수 있도록 하였습니다.
- pagination은 DRF에서 기존적으로 제공하는 LimitOffsetPagination을 사용했습니다.
- DRF로 구현한 장점은 기본적인 요소가 이미 구현이 되어 있어서 사용자가 필요한 부분만 부분적으로 커스텀하여 만들 수 있기 때문에, 생산성 향상에 도움을 주어 DRF를 선택해서 구현하였습니다.

## 실행방법
1. miniconda를 설치한다. ([https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html))
2. 해당프로젝트를 clone 하고, 프로젝트 폴더로 들어간다.
    
    ```bash
    git clone https://github.com/jotasic/wecode_wanted
    cd wecode_wanted
    ```
    
3. 가상환경을 만들고 필요한 프로젝트 구축에 필요한 패키지를 설치한다.
    
    ```bash
    conda create --name wecode_wanted python=3.8
    conda activate wecode_wanted
    pip install -r requirements.txt
    ```
    
4. db에 테이블을 구축한다. 
    
    ```bash
    python manage.py migrate
    ```
    
5. 서버를 실행한다.
    
    ```bash
    python manage.py runserver 0.0.0.0:8000
    ```
    

## API

### 회원가입

회원 가입을 한다

**POST /account/registration**

- body
    - email : 회원 email
    - password : 비밀번호
    - nickname : 닉네임

```bash
# request
curl --header 'Content-Type: application/json;' \
--request POST "localhost:8000/account/registration" \
--data-raw '{
    "email" : "test1@gmail.com",
    "password" : "12345678",
    "nickname" : "테스트"
}'

# response
{
  "id": 2,
  "last_login": null,
  "email": "test1@gmail.com",
  "nickname": "테스트",
  "date_of_join": "2021-10-22",
  "is_admin": false
}
```

### 로그인 (토큰 획득)

글작성 삭제 변경에 필요한 토큰을 획득한다.

**POST /account/token**

- body
    - email : 회원 email
    - password : 비밀번호

```bash
# request
curl --header 'Content-Type: application/json;' \
--request POST "localhost:8000/account/token" \
--data-raw '{
    "email" : "test1@gmail.com",
    "password" : "12345678"
}'

# response
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 토큰 갱신

만료된 토큰을 갱신한다.

**POST /account/token/refresh**

- body
    - refresh : 로그인(토큰 획득) 시에 획득한 refresh token 입력

```bash
# request
curl --header 'Content-Type: application/json;' \
--request POST "localhost:8000/account/token/refresh" \
--data-raw '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIU..."
}'

# response
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJI..."
}
```

### 리스트 조회

포스트들을 조회한다. 조회만 하기때문에 Access Token이 필요없다.

**GET /posts?limit={조회 갯수}&offset={조회 시작 위치}**

```bash
# request
curl --request GET "localhost:8000/posts?limit=30&offset=0"

# response
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "안녕하세요",
      "content": "반갑습니다!",
      "created_at": "2021-10-21T17:41:59.107277",
      "edited_at": "2021-10-21T17:41:59.107324"
    },
    {
      "id": 3,
      "author": "원티드",
      "title": "안녕하세요",
      "content": "내용 바꿨음",
      "created_at": "2021-10-21T18:23:20.019602",
      "edited_at": "2021-10-21T18:27:17.923507"
    },
    {
      "id": 4,
      "author": "원티드",
      "title": "안녕하세요",
      "content": "반갑습니다! 하하하",
      "created_at": "2021-10-21T21:54:12.721167",
      "edited_at": "2021-10-21T21:54:12.721192"
    }
  ]
}
```

### 상세 조회

특정 포스트를 조회한다. 조회만 하기때문에 Access Token이 필요없다.

**GET /posts/{id}**

```bash
# request
curl --request GET "localhost:8000/posts/1"

# response
{
  "id": 1,
  "title": "안녕하세요",
  "content": "반갑습니다!",
  "created_at": "2021-10-21T17:41:59.107277",
  "edited_at": "2021-10-21T17:41:59.107324"
}
```

### 포스트 작성

포스트를 작성한다.

**POST /posts**

- header에 token 입력
    - Authorization: Bearer {access token}
- body 내용
    - title : 포스트 타이틀
    - content : 포스트 내용

```bash
# request
curl --header 'Content-Type: application/json;' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLC...' 
--request POST "localhost:8000/posts" \
--data-raw '{
    "title" : "인사 드립니다",
    "content" : "안녕하세요"
}'

# response
{
  "id": 5,
  "author": "테스트",
  "title": "인사 드립니다",
  "content": "안녕하세요",
  "created_at": "2021-10-22T09:56:40.905027",
  "edited_at": "2021-10-22T09:56:40.905054"
}
```

### 포스트 내용 변경

포스트 내용을 변경한다. 변경을 할 내용만 입력한면 된다(tittle or content)

해당 내용을 작성한 user만 변경 가능하다.

**PATCH /posts/{id}**

- header에 token 입력
    - Authorization: Bearer {access token}
- body 내용
    - title : 포스트 타이틀
    - content : 포스트 내용

```bash
# request
curl --header 'Content-Type: application/json;' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLC...' \
 --request PATCH "localhost:8000/posts/5" \
 --data-raw '{
    "content" : "안녕하세요 좋은 아침입니다!"
}'

# response
{
  "id": 5,
  "author": "테스트",
  "title": "인사 드립니다",
  "content": "안녕하세요 좋은 아침입니다!",
  "created_at": "2021-10-22T09:56:40.905027",
  "edited_at": "2021-10-22T09:58:11.320511"
}
```

### 포스트 삭제

포스트를 삭제한다.

해당 내용을 작성한 user만 삭제 가능하다.

DELETE /posts/{id}

- header에 token 입력
    - Authorization: Bearer {access token}

```bash
# request
curl --header 'Content-Type: application/json;' \
--header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLC..' \
--request DELETE "localhost:8000/posts/5"
```

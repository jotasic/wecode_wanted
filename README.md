# [[위코드 x 원티드] 백엔드 프리온보딩 선발 과제]

## 과제 구현 내용
1. 글 작성, 글 확인, 글 목록 확인, 글 수정, 글 삭제가 되는 API
  - Delete과 Update는 해당 유저의 글만 가능
  - 즉, 유저 생성, 인가, 인증 기능도 필요
  - Read는 pagination 구현 필수
2. 데이터베이스는 in-memory database로 구현
  - 리뷰어가 Database를 따로 설치할 필요 없이 실행하고 확인할 수 있어야 합니다.
  - 예) sqlite3
3. Unit Test 구현시 가산점이 있습니다.
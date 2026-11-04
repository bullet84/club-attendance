# 모임 활동 신청·출석 관리

동아리·소모임의 활동 참가 신청부터 당일 출석 확인까지 하나의 흐름으로 연결하는 소프트웨어공학 학기 프로젝트입니다. `club-attendance`는 작업용 프로젝트 이름입니다.

## 프로젝트 목표

회원이 직접 참가 신청하면 신청자 명단에 반영되고, 운영진은 같은 명단에서 출석 상태를 변경합니다. 신청 명단을 별도의 출석부로 다시 옮기는 작업을 줄이는 것이 목표입니다.

## MVP 범위

1. 회원 명단 관리
2. 활동 생성
3. 회원의 직접 참가 신청
4. 활동별 신청자 명단 조회
5. 같은 신청자 명단을 이용한 출석 처리

관계형 DB의 `Group`, `Member`, `Activity`, `Participation`을 중심으로 설계합니다. 중간 발표 설계안에 따라 기존 세 테이블에 `Group`을 추가해 모임별 회원과 활동을 구분합니다. 같은 모임의 회원·활동만 연결하고 운영진 권한을 확인하는 것이 기본 설계입니다. 신청 취소, 신청 마감, 정원 제한, 출석률, 노쇼 집계, QR 출석, 통계는 후속 기능입니다.

## 현재 상태

2026년 11월 4일 기준, 첫 개발 기록과 SVG 도식을 작성하고 GitHub Pages용 개발 블로그를 구성했습니다. 모임 관리 서비스 코드와 DB는 아직 구현하지 않았으며 서비스 실행 명령과 URL은 준비되는 대로 추가합니다.

공개 저장소: [bullet84/club-attendance](https://github.com/bullet84/club-attendance)

개발 블로그: [모임의 기록](https://bullet84.github.io/club-attendance/)

Python Flask + SQLite를 초기 기술 후보로 검토하고 있습니다. 기술 선택, 회원 식별·모임별 운영진 권한, DB 제약조건은 구현 전에 구체화합니다.

## 개발 기록

- [개발 기록 전체 목차](docs/index.md)
- [1편. 참가 신청 명단을 그대로 출석부로 사용할 수 없을까?](docs/01-topic-proposal.md)

이후 DB 설계, 첫 서비스 배포, 최종 회고를 실제 진행 상황에 맞춰 기록합니다. GitHub Pages에는 개발 기록을 게시하며, 실제 모임 관리 서비스는 별도로 구현·배포합니다.

## 블로그 수정과 배포

`docs/*.md` 원문을 수정하고 `main`에 푸시하면 GitHub Actions가 HTML을 생성해 GitHub Pages에 배포합니다.

| 파일 | 역할 |
|---|---|
| `docs/01-topic-proposal.md` | 첫 블로그 원문 |
| `docs/assets/*.svg` | 본문 도식 |
| `site/config.json` | 사이트 이름과 글 목록·날짜·요약 |
| `site/templates/` | 홈과 본문 HTML 틀 |
| `site/assets/site.css` | 색상·레이아웃·모바일 스타일 |
| `scripts/build_site.py` | Markdown을 HTML로 변환 |
| `scripts/check_site.py` | 생성된 페이지의 내부 링크·이미지·목차 검사 |
| `.github/workflows/pages.yml` | 자동 빌드·검사·배포 |

새 글은 `docs/`에 작성하고 `site/config.json`에 제목·파일명·날짜·요약을 등록합니다. 미리 등록한 2~4편은 원문 파일이 생기면 공개 글로 전환됩니다. 게시할 때 예정 제목·요약을 실제 내용으로 바꾸고 날짜도 입력합니다. GitHub 문서 목차인 `docs/index.md`도 함께 갱신합니다.

### 로컬 미리보기 — Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-site.txt
.\.venv\Scripts\python.exe scripts/build_site.py
.\.venv\Scripts\python.exe scripts/check_site.py
.\.venv\Scripts\python.exe -m http.server 8765 --bind 127.0.0.1 --directory _site
```

브라우저에서 `http://127.0.0.1:8765/`를 엽니다. 수정 후 빌드 명령을 다시 실행하고 새로고침하면 됩니다. 생성된 `_site/`와 `.venv/`는 Git에 올리지 않습니다. 배포 진행 상태는 저장소의 **Actions → Publish development journal**에서 확인합니다.

## 진행 원칙

- 기능별로 작게 구현하고 검증하여 커밋 가능한 단위로 진행합니다.
- 설계 변경과 오류 해결 과정은 이유와 함께 기록합니다.
- 여러 종류의 모임에서 실제 사용한 뒤 운영진을 중심으로 평가합니다.
- 편의성·운영 부담·지속 사용 의향을 평가하며 시간 측정은 하지 않습니다.
- 실제 회원 정보, DB 파일, 비밀번호와 토큰은 저장소에 포함하지 않습니다.

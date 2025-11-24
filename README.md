# 연구실 안전관리 점검 자동화

이 프로젝트는 **전북대학교 연구실 안전관리시스템** 의  
일상 점검 절차를 **자동화**하기 위한 Python + Selenium 스크립트입니다.  
GitHub Actions를 이용해 **매주 월요일 오전 8시(한국시간)** 자동 실행되며,  
연구실 안전 점검 항목을 자동으로 클릭 및 저장합니다.

## 기능 요약

- Selenium을 이용한 **자동 로그인 및 점검 수행**
- GitHub Actions를 이용한 **매주 월요일 오전 8시 자동 실행**
- 각 단계별 **점검 로그 및 에러 코드 출력**
- 에러 발생 시 GitHub Actions 로그에 **자동 주석(::error)** 표시

## 동작 방식

1. `daily_auto_system.py`  
   - 웹사이트 접속 → 로그인 → 일상점검 페이지 진입 → 점검 항목 체크 → 저장  
   - 각 단계별 성공(`CHECK`) 또는 실패(`FAILED`) 로그 출력  

2. GitHub Actions (`.github/workflows/auto_inspection.yml`)  
   - 매일 오전 8시(KST)에 자동 실행 (`cron: "0 23 * * *"`)
   - 로컬 실행과 동일한 Python 환경 구성
   - Selenium + Chrome headless 모드로 동작
   - 실패 시 상세 오류 로그를 Actions에 출력

## 파일 구조
```
📂 .
├── daily_auto_system.py # 자동 점검 Python 코드
├── .github/
│ └── workflows/
│ └── auto_inspection.yml # GitHub Actions 워크플로 설정
└── README.md
```

## 환경 변수 설정(Github Secrets)
Actions 실행 시 로그인 정보를 보호하기 위해  
**GitHub Secrets**에 다음 두 항목을 추가해야 합니다.

| Name | Value | 예시 |
|------|--------|------|
| `ID` | 로그인 아이디 | `my_id` |
| `PASSWORD` | 로그인 비밀번호 | `my_password` |

📍 설정 위치  
`Repository → Settings → Secrets and variables → Actions`

## 에러 코드 표
| 코드      | 구간        | 설명                     |
| ------- | --------- | ---------------------- |
| 100~121 | 홈/로그인 진입  | 접속 또는 로그인 페이지 이동 실패    |
| 140~162 | 로그인 단계    | ID/PW 입력, 로그인 버튼 관련 오류 |
| 200~212 | 점검 페이지 이동 | 일상 점검/점검 화면 진입 실패      |
| 300~311 | 점검 클릭     | 체크박스 클릭 오류             |
| 400~402 | 저장 단계     | 저장 버튼 관련 오류            |
| 999     | 성공        | 전체 플로우 정상 종료           |

에러는 GitHub Actions 로그에서 ::error title=FAILED {code}:: 형식으로 표시됩니다.

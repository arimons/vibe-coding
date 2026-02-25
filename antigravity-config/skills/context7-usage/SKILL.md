---
name: context7-usage
description: Use when writing code that uses any external library or package for the first time in this project
---

# Context7 사용 규칙

## 조회해야 할 때 (Context7 사용)
- 이 프로젝트에서 해당 라이브러리를 처음 사용할 때
- 라이브러리 버전이 바뀐 후 첫 작업 시
- 에러가 "deprecated" 또는 버전 관련일 때

## 조회 불필요 (Context7 생략)
- 이미 이 세션에서 사용한 패턴 반복 시
- 기본 Python 문법 (조건문, 반복문, 함수 등)
- 이미 작동 중인 코드 패턴 재사용 시

## 절차
1. Context7에서 해당 라이브러리 최신 문서 조회
2. 현재 설치 버전 확인 (`pip show 패키지명`)
3. 버전에 맞는 문법으로 코드 작성
4. 사용한 버전을 주석으로 명시

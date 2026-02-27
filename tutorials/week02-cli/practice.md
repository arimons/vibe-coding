# Week 2 실습 - CLI 기초

> 개념 먼저 읽고 왔나요? → [CLI 기초 가이드](https://arimons.github.io/vibe-coding/cli-guide/)  
> 퀴즈로 복습하고 싶다면 → [Week 2 실습 퀴즈](https://arimons.github.io/vibe-coding/week02-practice/)

---

## 미션 1 — 기초 탐색 + 백업

**실습 폴더로 이동하세요:**

```powershell
cd C:\Users\amore\dev\vibe-coding\tutorials\week02-cli\practice\01_backup\data
```

**초기 상태**
```
01_backup/data/
├── sample_A_week1.csv
├── sample_A_week4.csv
├── sample_B_week1.csv
├── sample_B_week4.csv
└── report_draft.txt
```

**목표 상태**
```
01_backup/data/
├── sample_A_week1.csv
├── sample_A_week4.csv
├── sample_B_week1.csv
├── sample_B_week4.csv
├── report_draft.txt
└── backup_0225/
    ├── sample_A_week1_backup.csv
    ├── sample_A_week4_backup.csv
    ├── sample_B_week1_backup.csv
    └── sample_B_week4_backup.csv
```

> 오늘 분석 작업 전 원본 파일을 백업해두려 합니다.  
> `backup_0225` 폴더를 만들고 csv 파일만 골라서 복사한 뒤, 파일 이름에 `_backup`을 붙여두세요.  
> `report_draft.txt`는 백업 대상이 아닙니다.

---

**Step 1.** 현재 폴더에 어떤 파일이 있는지 확인하세요.

**Step 2.** `backup_0225` 폴더를 만드세요.

**Step 3.** csv 파일 4개를 한 번에 `backup_0225` 폴더로 복사하세요.  
힌트: `*`

**Step 4.** `backup_0225` 폴더로 이동해서 파일이 잘 복사됐는지 확인하세요.

**Step 5.** 파일 4개의 이름을 각각 `_backup`이 붙은 이름으로 바꾸세요.

**Step 6.** 다시 `data` 폴더로 돌아와 원본 파일이 그대로인지 확인하세요.

---

## 미션 2 — 뒤섞인 파일 정리

**실습 폴더로 이동하세요:**

```powershell
cd C:\Users\amore\dev\vibe-coding\tutorials\week02-cli\practice\02_organize\data
```

**초기 상태**
```
02_organize/data/
├── sample_A_week1.csv
├── sample_A_week2.csv
├── sample_A_week3.csv
├── sample_A_week4.csv
├── sample_B_week1.csv
├── sample_B_week2.csv
├── sample_B_week3.csv
├── sample_B_week4.csv
├── sample_C_week1.csv
├── sample_C_week2.csv
├── sample_C_week3.csv
└── sample_C_week4.csv
```

**목표 상태**
```
02_organize/data/
├── sample_A/
│   ├── sample_A_week1.csv
│   ├── sample_A_week2.csv
│   ├── sample_A_week3.csv
│   └── sample_A_week4.csv
├── sample_B/
│   └── ...
└── sample_C/
    └── ...
```

> 동료 연구원이 데이터를 한 폴더에 전부 받아뒀습니다.  
> sample A, B, C가 전부 섞여 있어 제출 전에 샘플별로 정리해달라는 요청을 받았습니다.  
> 각 샘플별 폴더를 만들고 파일을 분류하세요.

---

**Step 1.** 현재 폴더에 파일이 몇 개인지 확인하세요.

**Step 2.** `sample_A`, `sample_B`, `sample_C` 폴더를 만드세요.

**Step 3.** `sample_A`로 시작하는 파일을 `sample_A` 폴더로 한 번에 이동하세요.  
힌트: `*`

**Step 4.** 같은 방법으로 B, C도 정리하세요.

**Step 5.** 각 폴더 안에 파일이 4개씩 들어있는지 확인하세요.

---

## 미션 3 — 파일 병합과 스크립트 자동화

**실습 폴더로 이동하세요:**

```powershell
cd C:\Users\amore\dev\vibe-coding\tutorials\week02-cli\practice\03_script\data
```

**초기 상태**
```
03_script/data/
├── sample_A_week1.csv ~ sample_A_week4.csv
├── sample_B_week1.csv ~ sample_B_week4.csv
└── sample_C_week1.csv ~ sample_C_week4.csv
```

---

### 파트 A — 직접 이어붙이기

> sample_A의 week1~week4 데이터를 하나의 파일로 합쳐야 합니다.  
> `>>` 를 사용해서 `sample_A_merged.csv`를 만드세요.

**Step 1.** `sample_A_week1.csv` 내용을 `sample_A_merged.csv`로 복사하세요.  
힌트: `>`

**Step 2.** week2, week3, week4를 순서대로 `sample_A_merged.csv` 뒤에 이어붙이세요.  
힌트: `>>`

**Step 3.** 결과를 확인하세요.

```powershell
cat sample_A_merged.csv
```

> 헤더(`sample_id,week,...`)가 파일 중간에 반복해서 나타나는 것을 확인할 수 있습니다.  
> 수작업으로 이 문제를 해결하려면 각 파일마다 첫 줄을 따로 처리해야 합니다.  
> sample이 3개, 주차가 4개 — 총 12번 반복에 헤더 처리까지.  
> 이걸 깔끔하게 해결하는 게 파트 B입니다.

---

### 파트 B — LLM에게 스크립트 요청하기

> Claude나 ChatGPT에 아래 내용을 그대로 붙여넣고 스크립트를 받아보세요.

```
PowerShell 스크립트를 짜줘.

현재 폴더 안에 sample_A_week1.csv 부터 sample_C_week4.csv 형식의 파일이 12개 있어.
각 샘플(A, B, C)별로 week1~week4를 순서대로 이어붙여서
sample_A_merged.csv, sample_B_merged.csv, sample_C_merged.csv 를 만들어줘.
헤더(첫 번째 줄)는 첫 파일 것만 남기고 나머지 파일의 헤더는 제거해줘.
```

**Step 1.** 받은 스크립트를 `merge.ps1` 파일로 저장하세요.

**Step 2.** 스크립트를 실행하세요.

```powershell
.\merge.ps1
```

**Step 3.** 결과를 확인하세요.

```powershell
cat sample_B_merged.csv
```

**목표 상태**
```
03_script/data/
├── sample_A_week1.csv ~ sample_C_week4.csv  ← 원본 유지
├── sample_A_merged.csv   ← 헤더 1개, week1~4 데이터
├── sample_B_merged.csv
├── sample_C_merged.csv
└── merge.ps1
```

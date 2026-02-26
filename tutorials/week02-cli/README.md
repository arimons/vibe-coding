# Week 1 실습 - CLI 기초

## 실습 전 확인

PowerShell을 열고 실습 폴더로 이동하세요:

```powershell
cd C:\Users\amore\dev\vibe-coding\tutorials\week01-cli\practice
```

---

## 🎯 미션: 안정성 평가 데이터 백업하기

> **상황**: `data` 폴더에 안정성 평가 CSV 파일들이 있다.  
> 오늘 작업 전에 백업 폴더를 만들고, 백업본 이름을 `_backup` 을 붙여서 구분해두려 한다.

---

### Step 1. 지금 어떤 파일들이 있는지 확인해보세요.

<details>
<summary>정답 보기</summary>

```powershell
cd data
dir
```

`dir`은 PowerShell에서 `ls`와 동일해요.
</details>

---

### Step 2. `backup_0225` 폴더를 만들어보세요.

<details>
<summary>정답 보기</summary>

```powershell
mkdir backup_0225
```
</details>

---

### Step 3. `sample_A_week1.csv` 를 `backup_0225` 폴더로 복사해보세요.

<details>
<summary>정답 보기</summary>

```powershell
cp sample_A_week1.csv backup_0225\
```
</details>

---

### Step 4. `backup_0225` 폴더 안으로 이동해서 파일이 잘 복사됐는지 확인하세요.

<details>
<summary>정답 보기</summary>

```powershell
cd backup_0225
dir
```
</details>

---

### Step 5. 복사한 파일 이름을 `sample_A_week1_backup.csv` 로 바꿔보세요.

<details>
<summary>정답 보기</summary>

```powershell
mv sample_A_week1.csv sample_A_week1_backup.csv
```
</details>

---

### Step 6. 다시 `data` 폴더로 돌아가서 `.csv` 파일만 모두 `backup_0225` 로 복사해보세요.

<details>
<summary>정답 보기</summary>

```powershell
cd ..
cp *.csv backup_0225\
```

`*` 는 "아무 문자나" 를 의미해요. `*.csv` 는 `.csv` 로 끝나는 모든 파일이에요.
</details>

---

### Step 7. `backup_0225` 폴더 안의 파일이 몇 개인지 확인해보세요.

<details>
<summary>정답 보기</summary>

```powershell
dir backup_0225
```

4개의 csv + 1개의 이름 바뀐 파일, 총 5개가 보이면 성공!
</details>

---

## 🏆 도전 과제

`report_draft.txt` 도 `backup_0225` 에 복사하고, 이름을 `report_draft_0225.txt` 로 바꿔보세요.  
힌트 없이 혼자 해보세요!

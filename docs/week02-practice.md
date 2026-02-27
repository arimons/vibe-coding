---
layout: page
title: Week 2 실습 - CLI 기초
nav_order: 10
---

# Week 2 실습 - CLI 기초

📖 개념 먼저 읽고 오셨나요? → [CLI 기초 가이드](../cli-guide)

---

## 실습 전 준비

PowerShell을 열고 실습 폴더로 이동하세요:

```powershell
cd C:\Users\amore\dev\vibe-coding\tutorials\week02-cli\practice\01_backup\data
```

현재 위치 확인:

```powershell
pwd
```

---

## 📍 퀴즈: 명령어 맞히기

아래 상황을 읽고 어떤 명령어를 써야 할지 생각해보세요.

---

**Q1.** 터미널을 열었는데 내가 지금 어느 폴더에 있는지 모르겠다.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">pwd</code></pre>
현재 폴더의 전체 경로를 출력해줘요.
</details>

---

**Q2.** 현재 폴더 안에 어떤 파일과 폴더가 있는지 보고 싶다.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">dir</code></pre>
<code>dir</code>과 <code>ls</code> 둘 다 PowerShell에서 동작해요.
</details>

---

**Q3.** `Desktop` 폴더 안에 `research` 폴더가 있고, 그 안에 `2024` 폴더가 있다. 한 번에 이동하려면?

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cd Desktop\research\2024</code></pre>
</details>

---

**Q4.** 방금 들어온 폴더에서 한 단계 위로 나가고 싶다.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cd ..</code></pre>
두 단계 올라가려면 <code>cd ..\..</code>
</details>

---

**Q5.** 어디에 있든 홈 폴더(`C:\Users\amore`)로 바로 가고 싶다.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cd ~</code></pre>
</details>

---

**Q6.** `2024_Cosmetic_Stability_Test_Results`라는 폴더가 있다. 이 긴 이름을 전부 타이핑하지 않고 이동하려면?

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cd 2024[Tab]</code></pre>
<code>2024</code>까지만 치고 Tab을 누르면 자동완성돼요.<br>
여러 개가 있으면 Tab을 두 번 눌러서 후보 목록을 확인하세요.
</details>

---

**Q7.** 현재 폴더에 파일이 많은데 `.csv` 파일만 보고 싶다.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">dir *.csv</code></pre>
<code>*</code>는 "아무 문자나"를 의미해요. <code>*.csv</code>는 <code>.csv</code>로 끝나는 모든 파일이에요.
</details>

---

**Q8.** `sample_A_week1.csv`, `sample_A_week4.csv`, `sample_B_week1.csv` 중 `sample_A`로 시작하는 파일만 `backup` 폴더로 복사하고 싶다.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">mkdir backup
cp sample_A* backup\</code></pre>
</details>

---

## 🎯 미션: 안정성 평가 데이터 백업하기

> **상황**: `data` 폴더에 안정성 평가 CSV 파일 4개와 보고서 초안이 있다.  
> 오늘 작업 전에 백업 폴더를 만들고, 백업본임을 이름에 표시해두려 한다.

아래 단계를 순서대로 진행해보세요.

---

**Step 1.** 지금 `data` 폴더 안에 어떤 파일들이 있는지 확인하세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">dir</code></pre>
</details>

---

**Step 2.** `backup_0225` 폴더를 만드세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">mkdir backup_0225</code></pre>
</details>

---

**Step 3.** `sample_A_week1.csv`를 `backup_0225` 폴더로 복사하세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cp sample_A_week1.csv backup_0225\</code></pre>
</details>

---

**Step 4.** `backup_0225` 폴더 안으로 이동해서 파일이 잘 복사됐는지 확인하세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cd backup_0225
dir</code></pre>
</details>

---

**Step 5.** 복사한 파일 이름을 `sample_A_week1_backup.csv`로 바꾸세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">mv sample_A_week1.csv sample_A_week1_backup.csv</code></pre>
</details>

---

**Step 6.** 다시 `data` 폴더로 돌아가서 `.csv` 파일 4개를 모두 `backup_0225`로 복사하세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">cd ..
cp *.csv backup_0225\</code></pre>
</details>

---

**Step 7.** `backup_0225` 폴더 안의 파일이 몇 개인지 확인하세요.

<details>
<summary>정답 보기</summary>
<pre><code class="language-powershell">dir backup_0225</code></pre>
csv 4개 + 이름 바뀐 파일 1개, 총 5개가 보이면 성공!
</details>

---

## 🏆 도전 과제

`report_draft.txt`도 `backup_0225`에 복사하고, 이름을 `report_draft_0225.txt`로 바꿔보세요.  
힌트 없이 혼자 해보세요!

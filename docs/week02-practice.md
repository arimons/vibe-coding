---
layout: page
title: Week 2 실습 - CLI 기초
nav_order: 10
---

# Week 2 실습 - CLI 기초

📖 개념 먼저 읽고 오셨나요? → [CLI 기초 가이드](https://arimons.github.io/vibe-coding/cli-guide/)

---

## 📍 퀴즈: 명령어 맞히기

아래 상황을 읽고 어떤 명령어를 써야 할지 생각해보세요.

---

**Q1.** 터미널을 열었는데 내가 지금 어느 폴더에 있는지 모르겠다.

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">pwd</code></pre>
<p>현재 폴더의 전체 경로를 출력해줘요.</p>

</details>
{:/nomarkdown}

---

**Q2.** 현재 폴더 안에 어떤 파일과 폴더가 있는지 보고 싶다.

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">dir</code></pre>
<p><code>dir</code>과 <code>ls</code> 둘 다 PowerShell에서 동작해요.</p>

</details>
{:/nomarkdown}

---

**Q3.** `Desktop` 폴더 안에 `research` 폴더가 있고, 그 안에 `2024` 폴더가 있다. 한 번에 이동하려면?

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">cd Desktop\research\2024</code></pre>

</details>
{:/nomarkdown}

---

**Q4.** 방금 들어온 폴더에서 한 단계 위로 나가고 싶다.

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">cd ..</code></pre>
<p>두 단계 올라가려면 <code>cd ..\..</code></p>

</details>
{:/nomarkdown}

---

**Q5.** 어디에 있든 홈 폴더(`C:\Users\사용자이름`)로 바로 가고 싶다.

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">cd ~</code></pre>

</details>
{:/nomarkdown}

---

**Q6.** `2024_Cosmetic_Stability_Test_Results`라는 폴더가 있다. 이 긴 이름을 전부 타이핑하지 않고 이동하려면?

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">cd 2024[Tab]</code></pre>
<p><code>2024</code>까지만 치고 Tab을 누르면 자동완성돼요. 여러 개가 있으면 Tab을 두 번 눌러서 후보 목록을 확인하세요.</p>

</details>
{:/nomarkdown}

---

**Q7.** 현재 폴더에 파일이 많은데 `.csv` 파일만 보고 싶다.

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">dir *.csv</code></pre>
<p><code>*</code>는 "아무 문자나"를 의미해요. <code>*.csv</code>는 <code>.csv</code>로 끝나는 모든 파일이에요.</p>

</details>
{:/nomarkdown}

---

**Q8.** `sample_A_week1.csv`, `sample_A_week4.csv`, `sample_B_week1.csv` 중 `sample_A`로 시작하는 파일만 `backup` 폴더로 복사하고 싶다.

{::nomarkdown}
<details>

<summary>정답 보기</summary>

<pre><code class="language-powershell">mkdir backup
cp sample_A* backup\</code></pre>

</details>
{:/nomarkdown}

---

## 🎯 미션 1 — 기초 탐색 + 백업

**실습 폴더로 이동하세요:**

```powershell
cd C:\Developer\vibe-coding\tutorials\week02-cli\practice\01_backup\data
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

## 🎯 미션 2 — 뒤섞인 파일 정리

**실습 폴더로 이동하세요:**

```powershell
cd C:\Developer\vibe-coding\tutorials\week02-cli\practice\02_organize\data
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

## 🎯 미션 3 — 파일 병합과 스크립트 자동화

**실습 폴더로 이동하세요:**

```powershell
cd C:\Developer\vibe-coding\tutorials\week02-cli\practice\03_script\data
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

---

## 🎯 미션 4 — 로그 파일 탐색과 필터링

**실습 폴더로 이동하세요:**

```powershell
cd C:\Developer\vibe-coding\tutorials\week02-cli\practice\04_log_analysis
```

**초기 상태**
```
04_log_analysis/
├── server_log_01.log
├── server_log_02.log
├── ...
└── server_log_20.log
```

> 서버 로그 파일이 20개 쌓여 있습니다.  
> 운영팀에서 "지난 며칠간 WARN, ERROR 로그가 몇 건인지, 어떤 메시지가 가장 많이 나왔는지" 를 정리해달라는 요청을 받았습니다.  
> 파일을 하나씩 열어서 눈으로 세는 대신, CLI로 한 번에 처리해보세요.

---

**Step 1.** 파일이 몇 개인지 확인하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">dir *.log</code></pre>

</details>
{:/nomarkdown}

**Step 2.** `server_log_01.log` 파일 내용을 확인하세요. 어떤 형식인지 파악하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">cat server_log_01.log</code></pre>

</details>
{:/nomarkdown}

**Step 3.** 모든 로그 파일에서 `WARN`이 포함된 줄만 골라내세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">Select-String -Path *.log -Pattern "WARN"</code></pre>
<p>Mac/Linux라면: <code>grep "WARN" *.log</code></p>

</details>
{:/nomarkdown}

**Step 4.** WARN 로그만 골라내서 `warn_summary.txt` 파일로 저장하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">Select-String -Path *.log -Pattern "WARN" > warn_summary.txt
cat warn_summary.txt</code></pre>

</details>
{:/nomarkdown}

**Step 5.** WARN 로그가 총 몇 줄인지 세어보세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">Select-String -Path *.log -Pattern "WARN" | Measure-Object -Line</code></pre>

</details>
{:/nomarkdown}

**Step 6.** AI에게 스크립트를 요청해서 레벨별(INFO / WARN / DEBUG) 건수를 한 번에 집계해보세요.

```
PowerShell 스크립트를 짜줘.

현재 폴더에 server_log_01.log ~ server_log_20.log 파일이 있어.
각 파일을 읽어서 로그 레벨(INFO, WARN, DEBUG)별 총 건수를 집계하고
결과를 log_summary.txt로 저장해줘.
```

**목표 상태**
```
04_log_analysis/
├── server_log_01.log ~ server_log_20.log  ← 원본 유지
├── warn_summary.txt   ← WARN 로그만 모은 파일
└── log_summary.txt    ← 레벨별 집계 결과
```

---

## 🎯 미션 5 — 이미지 워터마크 일괄 처리

**실습 폴더로 이동하세요:**

```powershell
cd C:\Developer\vibe-coding\tutorials\week02-cli\practice\05_image_processing
```

**초기 상태**
```
05_image_processing/
├── test_image_1.jpg ~ test_image_10.jpg  ← 원본 이미지 10개
├── apply_watermark.py                    ← 워터마크 스크립트
└── apply_batch.sh                        ← 배치 실행 스크립트
```

> 보고서에 쓸 이미지 10개에 "Confidential" 워터마크를 찍어야 합니다.  
> 포토샵으로 하나씩 열어서 처리하는 대신, 스크립트로 한 번에 처리해보세요.

---

**Step 1.** 폴더 안의 파일 목록을 확인하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">dir</code></pre>

</details>
{:/nomarkdown}

**Step 2.** 가상환경을 만들고 활성화한 뒤, 필요한 패키지를 설치하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell"># 가상환경 생성
python -m venv .venv

# 가상환경 활성화
.venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt</code></pre>
<p>프롬프트 앞에 <code>(.venv)</code>가 붙으면 활성화 성공입니다.</p>
<p>Mac / Linux라면:</p>
<pre><code class="language-bash">python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt</code></pre>

</details>
{:/nomarkdown}

**Step 3.** 이미지 1개에만 먼저 워터마크를 적용해보세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">python apply_watermark.py test_image_1.jpg</code></pre>
<p>성공하면 <code>watermarked_test_image_1.jpg</code> 파일이 생깁니다.</p>

</details>
{:/nomarkdown}

**Step 4.** `watermarked_test_image_1.jpg`가 생성됐는지 확인하고, 탐색기에서 열어서 워터마크가 찍혔는지 확인하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">dir watermarked_*
# 탐색기로 열기
ii watermarked_test_image_1.jpg</code></pre>

</details>
{:/nomarkdown}

**Step 5.** 나머지 9개를 포함해 전체 이미지를 한 번에 처리하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<p><strong>방법 1 — Python으로 직접 실행 (Windows / Mac 공통)</strong></p>
<pre><code class="language-powershell">python apply_watermark.py all</code></pre>

<p><strong>방법 2 — 배치 스크립트 실행</strong></p>
<pre><code class="language-powershell"># Windows
.\apply_batch.ps1</code></pre>
<pre><code class="language-bash"># Mac / Linux
bash apply_batch.sh</code></pre>

> ⚠️ <code>python apply_batch.ps1</code> 또는 <code>python apply_batch.sh</code> 처럼
> 배치 스크립트를 python으로 실행하면 SyntaxError가 납니다.
> 배치 스크립트는 반드시 위의 방법으로 실행하세요.

</details>
{:/nomarkdown}

**Step 6.** 워터마크가 찍힌 파일이 10개 생성됐는지 확인하세요.

{::nomarkdown}
<details>

<summary>힌트</summary>

<pre><code class="language-powershell">dir watermarked_*</code></pre>
<p>10개가 보이면 성공입니다.</p>

</details>
{:/nomarkdown}

**목표 상태**
```
05_image_processing/
├── test_image_1.jpg ~ test_image_10.jpg         ← 원본 유지
├── watermarked_test_image_1.jpg ~ _10.jpg       ← 워터마크 결과물
├── apply_watermark.py
└── apply_batch.sh
```

> 💡 **CLI vs 포토샵**  
> 이미지 100개라면? 명령어 한 줄이면 됩니다.  
> 이게 CLI의 진짜 힘이에요.

---

## 🔗 다음 단계

미션 5의 워터마크 처리를 **브라우저에서 드래그앤드롭으로** 할 수 있다면 어떨까요?  
Week 3에서 이 스크립트를 Streamlit GUI로 감싸는 실습을 합니다.  
→ [Week 3 실습](https://arimons.github.io/vibe-coding/week03-gui/)

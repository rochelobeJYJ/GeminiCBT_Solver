# GeminiCBT Solver (Open Source)

Gemini Vision API를 활용한 스마트한 CBT 문제 풀이 도구입니다.

## 기능 (Features)

- **화면 캡처 (Screen Capture):** 원하는 영역을 쉽고 빠르게 드래그하여 캡처합니다.
- **AI 풀이 (AI Solver):** Google Gemini 2.0 Flash 모델이 실시간 스트리밍으로 정답과 해설을 제공합니다.
- **오버레이 (Overlay):** 캡처 영역을 시각적으로 명확하게 표시해 주는 가이드라인(Indicator)을 제공합니다.
- **편의성 (UX):** 항상 위 고정(Always on Top), 영역 표시 기능을 제공합니다.

## ScreenShot
<img width="520" height="650" alt="screenshot" src="https://github.com/user-attachments/assets/c72140f3-fb11-4631-aa0d-82a569a2b194" />
<img width="1362" height="646" alt="screenshot1" src="https://github.com/user-attachments/assets/f7792f5e-e65e-4064-a2dd-7dd2db1e5831" />

## 설치 및 실행 (Installation)

### [다운로드 (Releases)](https://github.com/사용자아이디/GeminiCBT_solver/releases)

위 링크에서 최신 버전(`GeminiCBT_solver.zip`)을 다운로드하고 실행하면 됩니다. (설치 X)

✨ 주요 기능 (Key Features)
📸 직관적인 캡처 (Screen Snip): 원하는 문제 영역을 마우스로 드래그하면 자동으로 인식합니다. 붉은색 가이드라인으로 캡처 영역을 명확하게 보여줍니다.
⚡ 실시간 스트리밍 (AI Streaming): 분석이 끝날 때까지 기다릴 필요가 없습니다. Gemini가 생각하는 대로 해설이 실시간으로 출력됩니다.
🎨 컴팩트 디자인 (Modern UI): 학습에 방해되지 않는 최적화된 창 크기와 깔끔한 UI를 제공합니다. '항상 위(Aleways on Top)' 기능을 지원합니다.
🔒 강력한 보안: API Key는 서버로 전송되지 않으며, 오직 사용자의 로컬 PC(AppData)에 암호화되어 저장됩니다.
📥 설치 및 실행 방법
아래 Assets 항목에서 GeminiCBT_solver.zip 파일을 다운로드합니다.
압축을 풀고 GeminiCBT_solver.exe를 실행합니다.
Google API Key를 입력하고(최초 1회), [영역 지정] 버튼을 눌러 문제를 선택하세요.



### 개발자용 실행 (For Developers)

1. **환경 설정**
   - Python 3.10 이상 필요

   ```bash
   pip install -r requirements.txt
   ```

2. **실행**

   ```bash
   python main.py
   ```

3. **빌드 (Build Executable)**

   ```bash
   build_v2.bat
   ```

## 라이선스 (License)

MIT License. 누구나 자유롭게 수정하고 배포할 수 있습니다.

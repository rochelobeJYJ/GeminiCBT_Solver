# GeminiCBT Solver (Open Source)

Gemini Vision API를 활용한 스마트한 CBT 문제 풀이 도구입니다.

## 기능 (Features)

- **화면 캡처 (Screen Capture):** 원하는 영역을 쉽고 빠르게 드래그하여 캡처합니다.
- **AI 풀이 (AI Solver):** Google Gemini 2.5/3.0 Flash 모델이 실시간 스트리밍으로 정답과 해설을 제공합니다.
- **오버레이 (Overlay):** 캡처 영역을 시각적으로 명확하게 표시해 주는 가이드라인(Indicator)을 제공합니다.
- **편의성 (UX):** 항상 위 고정(Always on Top), 다크/라이트 테마 자동 적용(시스템 설정), 단축키 지원 등을 고려했습니다.

## 설치 및 실행 (Installation)

### [다운로드 (Releases)](https://github.com/사용자아이디/GeminiCBT_solver/releases)

위 링크에서 최신 버전(`GeminiCBT_solver.zip`)을 다운로드하고 실행하면 됩니다. (설치 X)

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

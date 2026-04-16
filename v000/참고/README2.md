# 📌 DataNexus

유튜브 영상 및 텍스트 데이터를
**검색 및 질의응답이 가능한 형태로 변환하는 AI 데이터 파이프라인 시스템**

---

## 🚀 프로젝트 개요

DataNexus는 비정형 데이터(영상, 음성)를
텍스트로 변환하고 구조화하여
검색 및 질문 응답이 가능하도록 만드는 시스템입니다.

---

## 🖥️ 데모 화면

<!-- 여기에 스크린샷 이미지 넣기 -->

<!-- 예: ![demo](./assets/demo.png) -->

---

## ✨ 주요 기능

* 🎥 유튜브 링크 입력 → mp3 다운로드
* 🧠 Whisper 기반 STT (음성 → 텍스트)
* 💾 캐싱 시스템 (중복 다운로드 및 처리 방지)
* 🔍 텍스트 기반 검색 (추후 vector 검색 확장 예정)
* 💬 질문 → 답변 기능 (RAG, 구현 예정)

---

## ⚙️ 시스템 흐름

```plaintext
YouTube URL
→ Audio Download (yt-dlp)
→ Speech-to-Text (Whisper)
→ Text 저장 (cache)
→ (확장) Vector DB 저장
→ 검색 / 질문 응답
```

---

## 📂 프로젝트 구조

```plaintext
data33/
├── downloads/      # mp3 파일 저장
├── transcripts/    # STT 결과 저장
├── cache/          # 캐시 데이터

backend/
frontend/
```

---

## ⚙️ 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🧪 사용 방법

1. 유튜브 링크 입력
2. mp3 자동 다운로드
3. STT 실행 및 결과 생성
4. 동일 링크 재입력 시 캐시 활용

---

## 🎯 향후 계획

* Vector DB 기반 의미 검색 기능 추가
* RAG 기반 질문 응답 시스템 구현
* 영상 타임라인 기반 UI 개선
* YOLO / GPS 로그 데이터 연동

---

## 💡 핵심 아이디어

비정형 데이터(영상, 음성)를
검색 가능한 구조화 데이터로 변환하여
AI 기반 분석이 가능한 시스템 구축

---

## 🧩 기술 스택

* Python
* Streamlit
* yt-dlp
* Whisper
* (예정) FAISS / Chroma
* (예정) LangChain

---

## 📌 한 줄 요약

👉 “영상을 넣으면, 검색하고 질문할 수 있는 데이터로 바꿔주는 시스템”

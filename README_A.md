# 📌 프로젝트 개요

**프로젝트명:**
멀티 데이터 검색 & 분석 플랫폼
(AI 로그 검색 & 분석 시스템)

**목표:**
텍스트 및 로그 데이터를 구조화하여
검색 및 질문 응답이 가능한 RAG 시스템 구축

---

# 📌 핵심 기능

## 1. 데이터 입력

* 텍스트 파일 (.txt)
* PDF 문서
* (확장) 영상 → STT → 텍스트

---

## 2. 데이터 처리 파이프라인

[데이터 입력]
→ 텍스트 추출
→ chunk 분할
→ 메타데이터 생성
→ embedding 생성
→ vector DB 저장

---

## 3. 기능

* 키워드 검색
* 의미 기반 검색 (Vector Search)
* 질문 → 답변 (RAG)
* 문서 요약

---

# 📌 시스템 구조

## Backend

* FastAPI
* 파일 업로드 API
* 검색 API
* RAG 처리

## Frontend

* React (or Streamlit)
* 검색 UI
* 결과 시각화

## AI / 데이터

* Embedding: OpenAI or Local
* Vector DB: FAISS / Chroma
* Pipeline: LangChain

## 기타

* STT: Whisper
* 파일 처리: Python

---

# 📌 프로젝트 구조

project/

backend/

* main.py
* api/
* rag/
* models/
* utils/

frontend/

* src/
* components/

data/

* raw/
* processed/
* vector_store/

---

# 📌 핵심 흐름

[파일 업로드]
→ 텍스트 추출
→ chunk 분할
→ embedding 생성
→ vector DB 저장

[사용자 질문]
→ 유사 chunk 검색
→ LLM 응답 생성
→ 결과 반환

---

# 📌 역할 분배

## 데이터 / AI

* chunk 분할
* embedding 생성
* RAG 로직

## 백엔드

* FastAPI
* 파일 업로드 / 검색 API

## 프론트엔드

* 검색 UI
* 결과 표시

## (옵션)

* 영상 → STT 처리

---

# 📌 최종 목표

* 텍스트 / PDF 업로드
* 벡터 기반 검색
* 질문 → 답변 (RAG)

👉 "문서를 이해하고 답변하는 시스템" 구현


데모 시나리오

1. PDF 업로드
2. "이 문서 핵심 뭐야?" 질문
3. 답변 생성
4. 관련 문장 하이라이트

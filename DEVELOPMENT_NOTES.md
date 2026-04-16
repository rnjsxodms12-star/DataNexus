# Development Log

## 환경 설정

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 실행 테스트

* 테스트 링크:

  * https://youtu.be/Ot4dcoBOHWw

* 접속:

  * http://localhost:8501/

---

## 설치 이슈

* ffmpeg 필요

```bash
winget install ffmpeg
```

* imageio-ffmpeg 추가 설치 필요

```bash
pip install imageio-ffmpeg
```

---

## 초기 노트북 코드 (실험용)

```python
# pip install 및 실행 자동화 코드 (현재는 사용 안함)
```



유튜브 링크 주소를 입력하면 mp3파일을 다운로드 받고, STT동작을 실행하는데
여기서 나온 데이터를 캐쉬로 남겨서 1번 다운 받은 파일을 반복해서 다운받지 않게 만드는
노트북 또는 파일 또는 프로그램을 만들 수 있을까?
결과물은 위의 스크린샷 이미지와 비슷하면 좋겠어.
관련 파일은 data33 폴더로 모아줘.

requirements.txt

streamlit
yt-dlp
openai-whisper
imageio-ffmpeg
---

cd C:\Users\taeeun\.gemini\antigravity\scratch\33

pip install -r requirements.txt

python -m streamlit run app.py

enter

https://youtu.be/Ot4dcoBOHWw?si=3HchcqPg3cpAwDHA


http://localhost:8501/

winget install ffmpeg

y

cd C:\Users\taeeun\.gemini\antigravity\scratch\33

python -m streamlit run app.py

pip install imageio-ffmpeg

https://youtu.be/Ot4dcoBOHWw?si=-SB6jn1TgMUFaK6N


---
notebook_cord

import subprocess 
import sys 
# 필요한 패키지 설치 subprocess.run([sys.executable, '-m', 'pip', 'install', 'streamlit', 'yt-dlp', 'openai-whisper'], check=True) 
, 
# Streamlit 앱 실행 (터미널에서 실행하려면 아래 명령어를 사용하세요) 
# cd C:\Users\taeeun\Desktop\data33 
# python -m streamlit run app.py 
import subprocess 
import sys 
import os os.chdir(r'C:\Users\taeeun\Desktop\data33') subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', 'app.py']) 
print('Streamlit 앱이 시작되었습니다! 브라우저에서 http://localhost:8501 을 열어주세요.') 
, 
python -m streamlit run app.py


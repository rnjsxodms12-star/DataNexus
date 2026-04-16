import streamlit as st
import yt_dlp
import whisper
import os
import json
import re

# ffmpeg 실행 파일 경로 (로컬에 다운로드된 바이너리 사용)
FFMPEG_DIR = os.path.dirname(os.path.abspath(__file__))

# 캐시 및 다운로드 폴더 설정
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# 페이지 설정
st.set_page_config(page_title="YouTube STT 뷰어", layout="wide", page_icon="🎬")

st.markdown("""
<style>
    .stApp { background-color: #0f0f11; }
    .main-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 4px;
    }
    .sub-title {
        font-family: 'Segoe UI', sans-serif;
        font-size: 0.95rem;
        color: #94a3b8;
        margin-bottom: 24px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🎬 YouTube 자동 STT (음성 인식)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">유튜브 링크를 입력하면 Whisper AI가 자동으로 스크립트를 추출합니다. 타임스탬프를 클릭하면 해당 시간대로 이동합니다.</div>', unsafe_allow_html=True)

url = st.text_input("유튜브 링크", placeholder="🔗 유튜브 링크를 입력하세요 (예: https://www.youtube.com/watch?v=...)", label_visibility="collapsed")

@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def get_video_id(url):
    match = re.search(r"(?:v=|youtu\.be\/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

if url:
    video_id = get_video_id(url)
    if not video_id:
        st.error("올바른 유튜브 링크가 아닙니다.")
        st.stop()

    audio_path = os.path.join(CACHE_DIR, f"{video_id}.mp3")
    transcript_path = os.path.join(CACHE_DIR, f"{video_id}.json")

    status_bar = st.empty()

    try:
        # --- 1. MP3 다운로드 ---
        if not os.path.exists(audio_path):
            status_bar.info("🎵 유튜브 영상에서 음성(MP3)을 다운로드 중입니다. 잠시만 기다려주세요...")
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'ffmpeg_location': FFMPEG_DIR,
                'outtmpl': os.path.join(CACHE_DIR, f"{video_id}.%(ext)s"),
                'quiet': True,
                'no_warnings': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        # --- 2. STT 변환 ---
        if not os.path.exists(transcript_path):
            status_bar.info("🗣️ AI가 음성을 텍스트로 변환 중입니다. 영상 길이에 따라 수 분이 걸릴 수 있습니다...")
            model = load_whisper_model()
            result = model.transcribe(audio_path)
            with open(transcript_path, "w", encoding="utf-8") as f:
                json.dump(result["segments"], f, ensure_ascii=False, indent=4)
            status_bar.success("✨ 변환 완료!")
            segments = result["segments"]
        else:
            status_bar.success("✅ 캐시에서 불러왔습니다!")
            with open(transcript_path, "r", encoding="utf-8") as f:
                segments = json.load(f)

        segments_json = json.dumps(segments, ensure_ascii=False)

        # --- 3. 인터랙티브 UI ---
        html_component = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="utf-8">
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
                background: #0f0f11;
                color: #f1f5f9;
                padding: 8px;
            }}

            .container {{
                display: flex;
                gap: 16px;
                height: 520px;
            }}

            /* 비디오 패널 */
            .video-panel {{
                flex: 1.4;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}

            #player-wrapper {{
                flex: 1;
                border-radius: 14px;
                overflow: hidden;
                background: #000;
                box-shadow: 0 8px 32px rgba(0,0,0,0.5);
            }}

            #youtube-player {{
                width: 100%;
                height: 100%;
            }}

            .now-playing {{
                background: #1e293b;
                border: 1px solid #334155;
                border-radius: 10px;
                padding: 10px 14px;
                font-size: 13px;
                color: #94a3b8;
                min-height: 44px;
                display: flex;
                align-items: center;
                gap: 8px;
            }}

            .now-playing span {{
                color: #e2e8f0;
                font-weight: 500;
                flex: 1;
            }}

            /* 스크립트 패널 */
            .transcript-panel {{
                flex: 1;
                display: flex;
                flex-direction: column;
                background: #1a1d26;
                border: 1px solid #2d3347;
                border-radius: 14px;
                overflow: hidden;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}

            .panel-header {{
                padding: 12px 14px;
                border-bottom: 1px solid #2d3347;
                display: flex;
                flex-direction: column;
                gap: 8px;
            }}

            .panel-title {{
                font-size: 13px;
                font-weight: 600;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}

            .search-row {{
                display: flex;
                gap: 8px;
                align-items: center;
            }}

            #search-input {{
                flex: 1;
                background: #0f1117;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 7px 12px;
                font-size: 13px;
                color: #e2e8f0;
                outline: none;
                transition: border-color 0.2s;
            }}

            #search-input::placeholder {{ color: #475569; }}
            #search-input:focus {{ border-color: #6366f1; }}

            .sync-btn {{
                padding: 7px 14px;
                border-radius: 8px;
                border: 1px solid #334155;
                background: #1e293b;
                color: #94a3b8;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
                white-space: nowrap;
            }}

            .sync-btn:hover {{ border-color: #6366f1; color: #a5b4fc; }}
            .sync-btn.on {{ background: #312e81; border-color: #6366f1; color: #a5b4fc; }}

            .result-count {{
                font-size: 11px;
                color: #475569;
                padding: 2px 0;
            }}

            .transcript-list {{
                flex: 1;
                overflow-y: auto;
                padding: 6px;
                scroll-behavior: smooth;
            }}

            .transcript-list::-webkit-scrollbar {{ width: 4px; }}
            .transcript-list::-webkit-scrollbar-track {{ background: transparent; }}
            .transcript-list::-webkit-scrollbar-thumb {{ background: #334155; border-radius: 4px; }}

            .segment {{
                display: flex;
                align-items: flex-start;
                gap: 10px;
                padding: 9px 10px;
                border-radius: 8px;
                cursor: pointer;
                transition: background 0.15s, transform 0.1s;
                margin-bottom: 2px;
                border-left: 3px solid transparent;
            }}

            .segment:hover {{
                background: #1e293b;
                transform: translateX(2px);
            }}

            .segment.active {{
                background: #1e1b4b;
                border-left-color: #6366f1;
            }}

            .segment.search-match {{
                background: #1c1a0e;
                border-left-color: #ca8a04;
            }}

            .timestamp {{
                background: #1e293b;
                color: #6366f1;
                padding: 3px 7px;
                border-radius: 6px;
                font-weight: 700;
                font-size: 12px;
                min-width: 46px;
                text-align: center;
                flex-shrink: 0;
                margin-top: 2px;
                font-family: 'Consolas', monospace;
                transition: all 0.2s;
                border: 1px solid #2d3347;
            }}

            .segment:hover .timestamp {{ background: #312e81; border-color: #6366f1; }}
            .segment.active .timestamp {{ background: #4f46e5; color: white; border-color: #4f46e5; }}

            .segment-text {{
                font-size: 13.5px;
                line-height: 1.65;
                color: #cbd5e1;
            }}

            .segment-text mark {{
                background: #ca8a04;
                color: #0f0f11;
                border-radius: 3px;
                padding: 0 2px;
                font-weight: 600;
            }}

            .no-results {{
                text-align: center;
                color: #475569;
                padding: 48px 20px;
                font-size: 14px;
            }}

            /* AI 질문 영역 스타일 */
            .main-wrapper {{
                display: flex;
                flex-direction: column;
                gap: 16px;
                height: 100%;
            }}
            .ai-panel {{
                background: #1a1d26;
                border: 1px solid #2d3347;
                border-radius: 14px;
                padding: 16px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }}
            .ai-title {{
                font-size: 14px;
                font-weight: 600;
                color: #a5b4fc;
                margin-bottom: 10px;
                display: flex;
                align-items: center;
                gap: 6px;
                letter-spacing: 0.05em;
            }}
            .ai-input-wrapper {{
                display: flex;
                gap: 8px;
            }}
            .ai-input-wrapper input {{
                flex: 1;
                background: #0f1117;
                border: 1px solid #334155;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #e2e8f0;
                outline: none;
                transition: border-color 0.2s;
            }}
            .ai-input-wrapper input:focus {{ border-color: #6366f1; }}
            .ai-input-wrapper button {{
                padding: 10px 20px;
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: background 0.2s;
                white-space: nowrap;
            }}
            .ai-input-wrapper button:hover {{ background: #4338ca; }}
            .ai-result {{
                margin-top: 14px;
                padding: 14px;
                background: #1e293b;
                border-radius: 8px;
                border-left: 4px solid #6366f1;
                font-size: 14px;
                line-height: 1.6;
            }}
            .ai-result-title {{
                font-weight: 700;
                color: #a5b4fc;
                margin-bottom: 6px;
            }}
            .ai-timestamp-btn {{
                display: inline-block;
                background: #312e81;
                color: #a5b4fc;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 700;
                cursor: pointer;
                border: 1px solid #4f46e5;
                margin-right: 6px;
                margin-top: 6px;
                font-family: 'Consolas', monospace;
                transition: all 0.2s;
            }}
            .ai-timestamp-btn:hover {{ background: #4f46e5; color: white; border-color: #a5b4fc; transform: translateY(-1px); }}
        </style>
        </head>
        <body>
            <div class="main-wrapper">
                <!-- AI 질문 영역 (상단) -->
                <div class="ai-panel">
                    <div class="ai-title">💬 질문 (AI 영역)</div>
                    <div class="ai-input-wrapper">
                        <input type="text" id="ai-input" placeholder="예: 고양이가 싫다고 한 부분 언제야? / 이 영상 핵심 요약해줘" onkeypress="if(event.key === 'Enter') simulateAI()" />
                        <button onclick="simulateAI()">질문하기</button>
                    </div>
                    <div id="ai-result" class="ai-result" style="display: none;"></div>
                </div>

                <!-- 기존 인터페이스 (중간 검색/비디오) -->
                <div class="container">
                    <!-- 비디오 패널 -->
                <div class="video-panel">
                    <div id="player-wrapper">
                        <div id="youtube-player"></div>
                    </div>
                    <div class="now-playing" id="now-playing">
                        🎬 <span id="now-text">재생 중인 구간이 여기 표시됩니다.</span>
                    </div>
                </div>

                <!-- 스크립트 패널 -->
                <div class="transcript-panel">
                    <div class="panel-header">
                        <div class="panel-title">📝 스크립트</div>
                        <div class="search-row">
                            <input type="text" id="search-input" placeholder="🔍 내용 검색..." oninput="onSearch()" />
                            <button class="sync-btn" id="sync-btn" onclick="toggleSync()">⏱ 동기화 OFF</button>
                        </div>
                        <div class="result-count" id="result-count"></div>
                    </div>
                    <div class="transcript-list" id="transcript-list"></div>
                </div>
                </div> <!-- End of container -->
            </div> <!-- End of main-wrapper -->

            <script>
                const segments = {segments_json};
                const videoId = "{video_id}";
                let player = null;
                let syncEnabled = false;
                let syncInterval = null;
                let currentActiveIndex = -1;

                // YouTube IFrame API 로드
                var tag = document.createElement('script');
                tag.src = "https://www.youtube.com/iframe_api";
                document.head.appendChild(tag);

                function onYouTubeIframeAPIReady() {{
                    player = new YT.Player('youtube-player', {{
                        videoId: videoId,
                        width: '100%',
                        height: '100%',
                        playerVars: {{ 'playsinline': 1, 'rel': 0, 'modestbranding': 1 }},
                        events: {{
                            'onStateChange': onPlayerStateChange
                        }}
                    }});
                }}

                function onPlayerStateChange(event) {{
                    if (event.data === YT.PlayerState.PLAYING && syncEnabled) {{
                        startSync();
                    }}
                }}

                function seekTo(seconds, index) {{
                    if (player && player.seekTo) {{
                        player.seekTo(seconds, true);
                        player.playVideo();
                        if (!syncEnabled) {{
                            highlightSegment(index);
                        }}
                    }}
                }}

                function toggleSync() {{
                    syncEnabled = !syncEnabled;
                    const btn = document.getElementById('sync-btn');
                    if (syncEnabled) {{
                        btn.textContent = '✅ 동기화 ON';
                        btn.classList.add('on');
                        startSync();
                    }} else {{
                        btn.textContent = '⏱ 동기화 OFF';
                        btn.classList.remove('on');
                        stopSync();
                    }}
                }}

                function startSync() {{
                    stopSync();
                    syncInterval = setInterval(() => {{
                        if (!player || !player.getCurrentTime) return;
                        const t = player.getCurrentTime();
                        let activeIdx = -1;
                        for (let i = segments.length - 1; i >= 0; i--) {{
                            if (t >= segments[i].start) {{ activeIdx = i; break; }}
                        }}
                        if (activeIdx !== currentActiveIndex) {{
                            currentActiveIndex = activeIdx;
                            highlightSegment(activeIdx);
                            if (activeIdx >= 0) {{
                                const el = document.querySelector(`.segment[data-index="${{activeIdx}}"]`);
                                if (el) el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                            }}
                        }}
                    }}, 400);
                }}

                function stopSync() {{
                    if (syncInterval) {{ clearInterval(syncInterval); syncInterval = null; }}
                }}

                function highlightSegment(index) {{
                    document.querySelectorAll('.segment').forEach(el => el.classList.remove('active'));
                    const el = document.querySelector(`.segment[data-index="${{index}}"]`);
                    if (el) {{
                        el.classList.add('active');
                        const text = segments[index]?.text?.trim() || '';
                        document.getElementById('now-text').textContent = text;
                    }}
                }}

                function formatTime(sec) {{
                    const m = Math.floor(sec / 60);
                    const s = Math.floor(sec % 60);
                    return m + ':' + String(s).padStart(2, '0');
                }}

                function escapeRegex(str) {{
                    return str.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
                }}

                function onSearch() {{
                    const q = document.getElementById('search-input').value.trim().toLowerCase();
                    renderSegments(q);
                }}

                function simulateAI() {{
                    const query = document.getElementById('ai-input').value.trim();
                    if (!query) return;
                    
                    const resultDiv = document.getElementById('ai-result');
                    resultDiv.style.display = 'block';
                    resultDiv.innerHTML = '<div style="color:#94a3b8;">AI가 영상을 분석하고 있습니다... ⏳</div>';
                    
                    setTimeout(() => {{
                        if (query.includes('요약')) {{
                            resultDiv.innerHTML = `
                                <div class="ai-result-title">📌 답변:</div>
                                <div>이 영상은 출근하기 싫은 마음을 고양이의 시선에서 재치 있게 표현한 짧은 브이로그 상황극입니다. 고양이(시루)를 만지며 출근을 미루고 싶어 하는 모습이 담겨 있습니다.</div>
                            `;
                            return;
                        }} 
                        
                        // 자연어 질문에서 검색할 키워드를 흉내내어 추출하는 로직
                        let keyword = "";
                        
                        // 1. 따옴표로 감싼 단어 찾기
                        let match = query.match(/['"](.*?)['"]/);
                        if (match) {{
                            keyword = match[1];
                        }} else {{
                            // 2. "출근이라는 말은 언제" -> "출근" 추출
                            let kwMatch = query.match(/(.+?)(이)?라는\s*(말은|부분|단어)/);
                            if (kwMatch) {{
                                keyword = kwMatch[1].trim();
                            }} else {{
                                // 3. "출근 언제" -> "출근" 추출
                                let kwMatch2 = query.match(/(.+?)(은|는|이|가|\s)+\s*언제/);
                                if (kwMatch2) keyword = kwMatch2[1].trim();
                            }}
                        }}
                        
                        // 예외 처리용 추가 추출 (정규식 매칭 실패 시)
                        if (!keyword && query.includes('싫어')) keyword = '싫어';
                        if (!keyword && query.includes('출근')) keyword = '출근';

                        if (keyword) {{
                            let matches = [];
                            segments.forEach((seg, i) => {{
                                if (seg.text.includes(keyword)) matches.push({{ start: seg.start, index: i }});
                            }});
                            
                            if (matches.length > 0) {{
                                let textHtml = `<div class="ai-result-title">📌 답변:</div>`;
                                textHtml += `<div>영상에서 <strong>'${{keyword}}'</strong>(이)가 언급된 구간은 다음과 같습니다:</div><div style="margin-top: 4px;">`;
                                
                                matches.slice(0, 10).forEach(m => {{
                                    textHtml += `<span class="ai-timestamp-btn" onclick="seekTo(${{m.start}}, ${{m.index}})">👉 [${{formatTime(m.start)}}]</span>`;
                                }});
                                textHtml += `</div>`;
                                resultDiv.innerHTML = textHtml;
                            }} else {{
                                 resultDiv.innerHTML = `<div class="ai-result-title">📌 답변:</div><div>영상 스크립트 내에서 '${{keyword}}'(이)라는 내용을 찾을 수 없습니다.</div>`;
                            }}
                        }} else {{
                             // 4. 형태소 분석 우회 - 의미 있는 단어를 나눠서 하나라도 걸리는지 매칭
                             const words = query.replace(/[?!.,]/g, '').split(' ').filter(w => w.length > 1 && !w.includes('언제') && !w.includes('어디') && !w.includes('누가') && !w.includes('나와'));
                             
                             let foundMatches = [];
                             let foundWord = "";
                             for (let word of words) {{
                                 segments.forEach((seg, i) => {{
                                     if (seg.text.includes(word)) foundMatches.push({{ start: seg.start, index: i }});
                                 }});
                                 if (foundMatches.length > 0) {{
                                     foundWord = word;
                                     break;
                                 }}
                             }}

                             if (foundMatches.length > 0) {{
                                 let textHtml = `<div class="ai-result-title">📌 답변:</div>`;
                                 textHtml += `<div>질문하신 내용과 관련하여 <strong>'${{foundWord}}'</strong>(이)가 포함된 구간을 찾았습니다:</div><div style="margin-top: 4px;">`;
                                 foundMatches.slice(0, 10).forEach(m => {{
                                     textHtml += `<span class="ai-timestamp-btn" onclick="seekTo(${{m.start}}, ${{m.index}})">👉 [${{formatTime(m.start)}}]</span>`;
                                 }});
                                 textHtml += `</div>`;
                                 resultDiv.innerHTML = textHtml;
                             }} else {{
                                 resultDiv.innerHTML = `<div class="ai-result-title">📌 답변:</div><div>"${{query}}"에 대한 명확한 답변을 영상에서 찾을 수 없습니다. (RAG 백엔드 연동 전 데모입니다.)</div>`;
                             }}
                        }}
                    }}, 800);
                }}

                function renderSegments(query = '') {{
                    const list = document.getElementById('transcript-list');
                    list.innerHTML = '';
                    let count = 0;

                    segments.forEach((seg, i) => {{
                        const text = seg.text.trim();
                        const lower = text.toLowerCase();
                        if (query && !lower.includes(query)) return;
                        count++;

                        const div = document.createElement('div');
                        div.className = 'segment' + (query ? ' search-match' : '');
                        div.dataset.index = i;
                        div.onclick = () => seekTo(seg.start, i);

                        const ts = document.createElement('span');
                        ts.className = 'timestamp';
                        ts.textContent = formatTime(seg.start);

                        const tx = document.createElement('span');
                        tx.className = 'segment-text';
                        if (query) {{
                            const re = new RegExp(`(${{escapeRegex(query)}})`, 'gi');
                            tx.innerHTML = text.replace(re, '<mark>$1</mark>');
                        }} else {{
                            tx.textContent = text;
                        }}

                        div.appendChild(ts);
                        div.appendChild(tx);
                        list.appendChild(div);
                    }});

                    const rc = document.getElementById('result-count');
                    if (query) {{
                        rc.textContent = count > 0 ? `"${{query}}" — ${{count}}개의 결과` : '';
                    }} else {{
                        rc.textContent = `총 ${{segments.length}}개 구간`;
                    }}

                    if (count === 0) {{
                        list.innerHTML = '<div class="no-results">🔍 검색 결과가 없습니다.</div>';
                    }}
                }}

                renderSegments();
            </script>
        </body>
        </html>
        """

        st.components.v1.html(html_component, height=750, scrolling=False)

    except Exception as e:
        st.error(f"오류가 발생했습니다. 링크가 올바른지 확인해주세요. (상세 내역: {e})")

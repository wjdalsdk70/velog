from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import datetime
import os
import re

# === 설정 ===
MODEL_NAME = "mistral"
SAVE_DIR = "posts"  # 👉 저장 폴더 이름

# === LangChain LLM 설정 (Ollama 연결) ===
llm = Ollama(model=MODEL_NAME, temperature=0.8)

# === 프롬프트 템플릿 ===
template = """
You are a Korean health content creator writing expert-level, yet friendly blog posts.

Please write a blog post in **markdown format** based on the topic below.

Topic: "{topic}"

**Structure:**
1. 일상생활에서 이 주제와 관련해 발생할 수 있는 건강 문제
2. 이러한 문제가 이어질 수 있는 질병이나 증상
3. 이를 예방하거나 관리하는 방법 (예: 생활 습관, 운동, 음식 등)

**Style Requirements:**
- Language: Korean
- Tone: 친절하고 쉽게 설명하지만 신뢰감 있는 말투
- Include: 제목, 간단한 소개글, 부제목 포함 각 섹션 설명
- Markdown 사용: `#`, `##`, `-` 등 마크다운 요소 적극 활용
- 부가적으로 표나 코드블럭, 리스트 등이 유용하면 포함

Avoid repeating the topic too often, and ensure the flow feels natural and well-structured.
"""

prompt = PromptTemplate.from_template(template)

# === 응답 후처리 ===
def clean_output(text: str) -> str:
    text = text.strip()
    if len(text) < 100:
        return "[⚠️ 생성된 글이 너무 짧습니다. 다시 시도하세요.]\n" + text
    return text

# === 마크다운 저장 ===
def save_markdown(content: str, topic: str) -> str:
    os.makedirs(SAVE_DIR, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    safe_topic = re.sub(r"[^\w가-힣_]", "_", topic)
    filename = f"{SAVE_DIR}/{date_str}-{safe_topic}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 로컬에 저장 완료: {filename}")
    return filename

# === 실행 ===
if __name__ == "__main__":
    topic = input("블로그 주제를 입력하세요: ")
    final_prompt = prompt.format(topic=topic)
    print("✏️ LangChain을 통해 글 생성 중...\n")
    result = llm.invoke(final_prompt)
    cleaned = clean_output(result)
    save_markdown(cleaned, topic)
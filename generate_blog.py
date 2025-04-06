from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import datetime
import os
import re

# === 설정 ===
MODEL_NAME = "mistral"
SAVE_DIR = "posts"
PROMPT_FILE = "prompt_template.txt"

# === LangChain LLM 설정 (Ollama 연결) ===
llm = Ollama(model=MODEL_NAME, temperature=0.8)

# === 프롬프트 템플릿 로드 ===
def load_prompt_template(filepath: str) -> PromptTemplate:
    with open(filepath, "r", encoding="utf-8") as f:
        template_str = f.read()
    return PromptTemplate.from_template(template_str)

prompt = load_prompt_template(PROMPT_FILE)

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

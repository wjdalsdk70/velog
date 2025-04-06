from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
import datetime
import os
import re

def generate_blog(topic: str, save_dir="generated_articles"):
    llm = Ollama(model="mistral", temperature=0.8)

    template = """
    You are a Korean health content creator writing expert-level, yet friendly blog posts.

    Please write a blog post in **markdown format** about:
    "{topic}"

    Structure:
    1. 일상생활에서 이 주제와 관련해 발생할 수 있는 건강 문제
    2. 이러한 문제가 이어질 수 있는 질병이나 증상
    3. 이를 예방하거나 관리하는 방법 (예: 생활 습관, 운동, 음식 등)

    Use markdown headers, lists, and a friendly tone.
    """
    prompt = PromptTemplate.from_template(template)
    prompt_text = prompt.format(topic=topic)
    result = llm.invoke(prompt_text)

    # 저장
    os.makedirs(save_dir, exist_ok=True)
    safe_title = re.sub(r"[^\w가-힣]+", "_", topic)
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    path = os.path.join(save_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(result)
    return path
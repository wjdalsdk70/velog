import os
import re
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableSequence
from newspaper import Article

# 🔁 프롬프트 파일 로드 함수
def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# 🧠 Ollama LLM
llm = OllamaLLM(model="mistral")

# 📄 외부 프롬프트 로드
prompt_text = load_prompt("prompts/rewrite_blog_kr.prompt")
prompt = PromptTemplate.from_template(prompt_text)
chain = prompt | llm

# 📄 게시글 저장
def save_to_markdown(content: str):
    title_match = re.search(r'#\s*(.+)', content)
    title = title_match.group(1).strip() if title_match else f"untitled-{datetime.now().isoformat()}"
    slug = re.sub(r'\W+', '-', title.lower()).strip('-')
    filename = f"{datetime.now().strftime('%Y-%m-%d')}-{slug}.md"
    
    os.makedirs("posts", exist_ok=True)
    path = os.path.join("posts", filename)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ 저장 완료: {path}")

# 🌐 URL에서 본문 추출
def extract_article_text(url: str) -> str:
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# 🚀 전체 실행 함수
def recompose_from_url(url: str):
    original_text = extract_article_text(url)
    print(f"🔍 원문 길이: {len(original_text)}자")
    result = chain.invoke({"original_text": original_text})
    save_to_markdown(result)

# 🧪 테스트 실행
if __name__ == "__main__":
    test_url = input("원본 게시글 URL을 입력하세요: ")
    recompose_from_url(test_url)

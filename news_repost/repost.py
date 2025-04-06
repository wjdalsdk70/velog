import os
import re
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableSequence
from newspaper import Article
import requests
from bs4 import BeautifulSoup

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
import requests
from bs4 import BeautifulSoup
from newspaper import Article

def extract_article_text(url: str) -> str:
    try:
        # 1차 시도: newspaper3k
        article = Article(url)
        article.download()
        article.parse()
        if len(article.text.strip()) > 300:
            return article.text.strip()
    except Exception as e:
        print(f"newspaper 파싱 실패: {e}")

    # 2차 시도: BeautifulSoup
    print("📡 기본 파서 실패 → BeautifulSoup로 시도합니다...")
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # ✅ 조선일보 본문 selector 업데이트
    content_div = soup.select_one("div.article-body__content")

    if content_div:
        paragraphs = content_div.find_all("p")
        texts = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
        return "\n\n".join(texts)

    raise ValueError("❌ 기사 본문을 찾을 수 없습니다.")


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

import os
import re
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.runnables import RunnableSequence
from newspaper import Article

# 🧠 Ollama LLM
llm = OllamaLLM(model="mistral")

# 🧾 개선된 재작성 프롬프트
prompt = PromptTemplate.from_template("""
다음은 기존 블로그 게시글입니다.

--- 원문 ---
{original_text}
-------------

이 글을 다음 기준에 따라 **한국어 마크다운 블로그 글**로 재작성해 주세요:

1. 문체: 독자에게 친근한 설명체
2. 구조: `# 제목` → `## 요약` → `## 개념 설명` → `## 왜 중요한가?` → `## 예방법 / 관리법` → `## 마무리`
3. 자연스러운 흐름으로 문장을 이어가며, 문단은 적절히 나눠 주세요.
4. 내용 길이는 600~1000자 이상으로 풍부하게 써 주세요.
5. 필요하다면 마크다운 이미지 태그로 시각적 요소도 포함해 주세요. 예시:
   `![혈당 곡선 이미지](https://example.com/image.png)`

최종 결과는 완성된 **한국어 마크다운 블로그 글** 형식으로 출력해 주세요.
""")


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
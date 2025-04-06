from blog.generate_blog import generate_blog
from upload_to_notion import upload_markdown

if __name__ == "__main__":
    topic = input("블로그 주제를 입력하세요: ")
    md_path = generate_blog(topic)
    upload_markdown(md_path)
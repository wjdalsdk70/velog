import feedparser
import git
import os
import re
from datetime import datetime

# === 설정 ===
rss_url = 'https://api.velog.io/rss/@wjdalsdk70'
repo_path = os.getenv("VELOG_REPO_PATH", '.')  # GitHub Actions용 환경변수 사용 가능
posts_dir = os.path.join(repo_path, 'velog-posts')

# === 폴더 준비 ===
os.makedirs(posts_dir, exist_ok=True)

# === 깃 저장소 로드 ===
repo = git.Repo(repo_path)

# === RSS 파싱 ===
feed = feedparser.parse(rss_url)

# === 글 저장 및 커밋 ===
def sanitize_filename(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|]', '_', name)  # 윈도우에서 불가한 문자 제거
    return name.strip()

for entry in feed.entries:
    title = entry.title
    file_name = sanitize_filename(title) + '.md'
    file_path = os.path.join(posts_dir, file_name)

    if not os.path.exists(file_path):
        # 날짜 포맷 파싱 (RFC822 → ISO8601)
        date = datetime(*entry.published_parsed[:6]).isoformat()

        # YAML Frontmatter 생성
        frontmatter = f"""---
title: "{title}"
date: {date}
tags: []
---

"""

        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + entry.description)

        # Git 작업
        repo.git.add(file_path)
        repo.index.commit(f"Add post: {title}")
        print(f"✅ 저장 및 커밋: {file_name}")
    else:
        print(f"🔹 이미 존재함: {file_name}")

# === 푸시 ===
try:
    repo.remote(name='origin').push()
    print("🚀 GitHub 푸시 완료")
except Exception as e:
    print(f"❌ 푸시 실패: {e}")
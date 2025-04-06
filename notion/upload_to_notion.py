from notion_client import Client
import os
import markdown
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

notion = Client(auth=NOTION_TOKEN)

def upload_markdown(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 제목 추출 (마크다운의 첫 # )
    title = "Untitled"
    for line in content.splitlines():
        if line.startswith("# "):
            title = line[2:]
            break

    # 본문을 여러 블록으로 나누기 (한 블록 1800자 이하)
    def split_text(text, max_len=1800):
        parts = []
        while len(text) > max_len:
            split_at = text.rfind("\n", 0, max_len)
            split_at = split_at if split_at != -1 else max_len
            parts.append(text[:split_at])
            text = text[split_at:].lstrip()
        parts.append(text)
        return parts

    paragraphs = split_text(content)

    blocks = [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {"content": p}
                    }
                ]
            }
        } for p in paragraphs
    ]

    response = notion.pages.create(
        parent={"page_id": NOTION_PAGE_ID},
        properties={
            "title": [{"type": "text", "text": {"content": title}}]
        },
        children=blocks
    )

    print(f"✅ Uploaded to Notion: {response['url']}")

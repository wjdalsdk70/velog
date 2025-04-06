import shutil
from git import Repo
import os

def push_to_velog(local_md_path, velog_repo_path, commit_message="Add new blog post"):
    filename = os.path.basename(local_md_path)
    dest_path = os.path.join(velog_repo_path, filename)

    # 이미 같은 파일이 있으면 덮어쓰기
    if os.path.exists(dest_path):
        print(f"⚠️ 기존 파일 덮어쓰기: {dest_path}")
    shutil.copy(local_md_path, dest_path)
    print(f"✅ Velog 저장소로 복사 완료: {dest_path}")

    # Git 저장소 커밋 및 푸시
    try:
        repo = Repo(velog_repo_path)
        repo.git.add(filename)

        # 변경 사항이 있을 때만 커밋
        if repo.is_dirty(untracked_files=True):
            repo.index.commit(commit_message)
            origin = repo.remote(name='origin')
            origin.push()
            print("🚀 GitHub → Velog 블로그 푸시 완료!")
        else:
            print("🟡 변경 사항이 없어 푸시하지 않음.")
    except Exception as e:
        print(f"❌ Git 푸시 실패: {e}")

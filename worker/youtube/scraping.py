import os
import json
from googleapiclient.discovery import build
# TODO 動画を定期的に調べれるようにする
# Google APIキーを入力
API_KEY = ""

# YouTube Data APIのクライアントをビルド
# TODO envファイルから読み取れるようにする
youtube = build('youtube', 'v3', developerKey=API_KEY)

# videos.jsonファイルを読み込む
def load_existing_videos(json_file="videos.json"):
    
    if os.path.exists(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        return {}

# YouTube動画を検索してURLを取得
def search_youtube(query,video_duration="medium"):
    # YouTube APIを使って検索
    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",  # 追加: 動画のみを検索対象vvcにする
        maxResults=37, # 最大37件の動画を取得
        videoDuration=video_duration

    )
    response = request.execute()
    
    # 動画のURLをリストに追加
    video_urls = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)
    
    return video_urls

# 動画のURLを既存のものと照合し、新しいURLを取得して上書き
def update_video_urls(existing_videos, new_videos, json_file="videos.json"):
    # 新しい動画URLを追加（既存のURLと重複しないもの）
    updated_videos = existing_videos.copy()
    index = len(existing_videos) + 1  # インデックス番号の開始位置

    for url in new_videos:
        if url not in existing_videos.values():
            updated_videos[index] = url
            index += 1

    # 上書き保存
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(updated_videos, file, indent=4, ensure_ascii=False)
    
    return updated_videos

# 動物に関する動画を検索してURLを取得
new_videos = search_youtube("dogs action")

# videos.jsonから既存の動画URLを読み込む
existing_videos = load_existing_videos()

# 新しい動画URLを取得して、videos.jsonを更新
updated_videos = update_video_urls(existing_videos, new_videos)

# 更新後の動画URLを表示
print("Updated video URLs:")
for idx, url in updated_videos.items():
    print(f"{idx}: {url}")


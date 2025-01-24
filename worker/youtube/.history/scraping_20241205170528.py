import os
from googleapiclient.discovery import build

# Google APIキーを入力
API_KEY ="AIzaSyC7V49RhsD5o187DiA4th4Klhm_OJyCtFI" 

# YouTube Data APIのクライアントをビルド
youtube = build('youtube', 'v3', developerKey=API_KEY)

# "animal"に関連する動画を検索する
def search_youtube(query):
    # YouTube APIを使って検索
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=5  # 最大5件の動画を取得（任意の数に変更可能）
    )
    response = request.execute()
    
    # 動画のURLをリストに追加
    video_urls = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_urls.append(video_url)
    
    return video_urls

# "animal"に関連する動画を検索してURLを表示
videos = search_youtube("animal")
for video in videos:
    print(video)

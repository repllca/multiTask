import os
from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=oRDRfikj2z8&ab_channel=ScenicScenes"

# YouTube動画オブジェクトの作成
yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)

# 最も高画質なストリームを取得
ys = yt.streams.get_highest_resolution()

# 保存先ディレクトリ
output_directory = "./videos"  # 例: "C:/Downloads"

# ディレクトリ内の既存のファイル名を調べて次の番号を決定
existing_files = os.listdir(output_directory)
index = 1

# "videoX.mp4" という形式のファイル名が既に存在しているか確認
while f"video{index}.mp4" in existing_files:
    index += 1

# 新しいファイル名を設定
filename = f"video{index}.mp4"

# ファイルを指定したディレクトリと名前でダウンロード
ys.download(output_path=output_directory, filename=filename)

print(f"Downloaded as {filename}")


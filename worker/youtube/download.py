import os
import yt_dlp
def video_download(video_url, directory_path):
    """
    指定したYouTube URLの動画を指定したディレクトリにダウンロードします。
    ファイル名は "videoX.mp4" の形式で、自動的に連番を付けます。

    Args:
        video_url (str): ダウンロードするYouTube動画のURL。
        directory_path (str): 保存先のディレクトリパス。
    """

    # 保存先ディレクトリが存在しない場合は作成
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    try:
        # ディレクトリ内の既存のファイル名を調べて次の番号を決定
        existing_files = os.listdir(directory_path)
        index = 1
        while f"video{index}.mp4" in existing_files:
            index += 1

        # ファイル名に番号を付ける
        filename_template = f'{directory_path}/video{index}.%(ext)s'

        # yt-dlpのオプション設定
        options = {
            'outtmpl': filename_template,  # 動画のファイル名を連番で設定
            'format': 'best',              # 最も高画質を選択
            'progress_hooks': [on_progress] # 進行状況のコールバック関数を設定
        }

        # yt-dlpオブジェクトを作成し、動画をダウンロード
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([video_url])

        print(f"ダウンロードが完了しました: video{index}.mp4")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 進捗を表示するコールバック関数
def on_progress(d):
    if d['status'] == 'downloading':
        print(f"ダウンロード中: {d['filename']} - {d['_percent_str']}")

# 使用例
if __name__ == "__main__":
    # ダウンロードするYouTube動画のURL
    url = "https://www.youtube.com/watch?v=h64FiO3ME0Q"

    # 保存先ディレクトリ
    output_directory = "./tmp"
    for i in range(2):
    # 動画をダウンロード
        video_download(url, output_directory)


 


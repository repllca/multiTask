import redis
import json
import time
import os
import json
from youtube.download import video_download
from youtube.videoCutAnotation import process_video_and_generate_annotations
from youtube.cut import process_video_and_generate_annotations_cut
from youtube.send import transfer_directory
import re

def save_json_to_file(text, output_file_path):
    # 正規表現を使ってコードブロックを抽出
    json_string = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
    
    if json_string:
        # コードブロック部分を取得
        json_string = json_string.group(1)
        
        # 文字列が正しいJSONフォーマットになるようにデコード
        json_data = json.loads(json_string)

        # JSONをファイルに保存
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)
    else:
        print("JSONデータが見つかりませんでした。")

def clear_directory(directory_path):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # ファイルまたはリンクを削除
            elif os.path.isdir(file_path):
                os.rmdir(file_path)  # 空のディレクトリを削除
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")







# Redis接続情報
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379
# 処理内容
def process_task(task):
    """タスクを処理する関数"""
    print(f"Finished processing video {task['video_url']}")

    video_download(task["video_url"],"./tmp/")

    api_key = ""  # TODO: セキュリティのため、envファイルや別途設定で読み込むべき
    result = process_video_and_generate_annotations("./tmp/video1.mp4", api_key)
    # JSONを指定したファイルパスに保存
    output_json_path = "./tmp/annotations_result.json"  # 出力先のファイルパス

    save_json_to_file(result, output_json_path)

    process_video_and_generate_annotations_cut("./tmp/video1.mp4", "./tmp/annotations_result.json", "./output")


    local_dir = "./tmp"
    remote_dir = ""
    hostname = ""
    username = ""
    password = ""
    transfer_directory(local_dir=local_dir,remote_dir=remote_dir,hostname=hostname,username=username,password=password)
    clear_directory("./tmp") 
    print(f"Finished processing video {task['video_url']}")


def worker():
    """ワーカーのメインループ"""
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    print("Worker started, waiting for tasks...")
    
    while True:
        try:
            # キューからタスクを取得（ブロッキングモード）
            task_data = r.brpop("videos")
            
            # タスクをデコード
            task = json.loads(task_data[1])
            print("Processing task:", task)
            
            # タスクを処理（ここが終わるまで次のタスクは取得しない）
            process_task(task)
            
            print("Task completed. Ready for the next task.")
            
        except Exception as e:
            # エラー発生時の処理
            print(f"Error processing task: {e}")
            
            # 失敗したタスクを別のキューに移動
            if 'task_data' in locals():  # `task_data` が定義されている場合
                r.lpush("failed_videos", task_data[1])
                print("Task moved to failed tasks queue.")
            
            # エラー時に少し待機（スパム防止）
            time.sleep(2)

if __name__ == "__main__":
    worker()
import redis
import json

def add_task_to_queue(url):
    try:
        r = redis.Redis(host="localhost" , port=6379 , db=0)
        r.ping()  # 接続確認

        task_url = url.get("video_url")
        print(task_url)
        if not task_url:
            print("タスクにIDが含まれていません。")
            return

        # IDの重複チェック用セットのキー
        unique_task_set = "video_url"

        # IDがすでに存在するか確認
        if r.sismember(unique_task_set, task_url):
            print(f"タスクID {task_url} は既に存在します。")
        else:
            # IDをセットに追加
            r.sadd(unique_task_set, task_url)
                            # タスクをキューに追加
            r.lpush("videos", json.dumps(url))
            print("タスクを追加しました。")
    except redis.ConnectionError as e:
        print(f"Redisに接続できません: {e}")
    except Exception as e:
        print(f"タスクの追加中にエラーが発生しました: {e}")


#jsonをfor文で読み込む
with open('videos.json', 'r') as f:
    json_open = open('videos.json', 'r')
    json_load = json.load(json_open)

# print(json_load)
    for v in json_load.values():
        url_json = {"video_url": v}
        add_task_to_queue(url_json)


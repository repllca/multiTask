import redis
import json

def add_task_to_queue(task):
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)
        r.ping()  # 接続確認
        r.lpush("test", json.dumps(task))
        print("タスクを追加しました。")
    except redis.ConnectionError as e:
        print(f"Redisに接続できません: {e}")
    except Exception as e:
        print(f"タスクの追加中にエラーが発生しました: {e}")

# 例: タスクを追加
task = {"video_id": "12349", "action": "resize", "parameters": {"width": 1280, "height": 720}}
add_task_to_queue(task)


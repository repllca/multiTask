import redis
import json
import time
import os

# Redis接続情報
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379

def process_task(task):
    """タスクを処理する関数"""
    print(f"Processing video {task['video_id']} with action {task['action']}")
    time.sleep(2)  # 処理のシミュレーション
    print(f"Finished processing video {task['video_id']}")

def worker():
    """ワーカーのメインループ"""
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    print("Worker started, waiting for tasks...")
    
    while True:
        # キューからタスクを取得（ブロッキングモード）
        task_data = r.brpop("test")
        
        # タスクをデコード
        task = json.loads(task_data[1])
        
        # タスクを処理
        try:
            process_task(task)
        except Exception as e:
            print(f"Error processing task: {e}")

if __name__ == "__main__":
    worker()

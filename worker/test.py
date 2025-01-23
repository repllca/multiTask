import redis

def test_redis_connection():
    try:
        r = redis.Redis(host="localhost", port=6379, db=0)  # 必要に応じて host を変更
        r.ping()  # Redis サーバーへの接続をテスト
        print("Redis に接続成功！")
    except redis.ConnectionError as e:
        print(f"Redis に接続できません: {e}")

test_redis_connection()

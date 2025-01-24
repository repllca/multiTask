import paramiko
from scp import SCPClient

def transfer_directory(local_dir, remote_dir, hostname, username, password):
    """
    SCPを使ってローカルのディレクトリをリモートサーバーに転送する関数
    ディレクトリを再帰的に転送します。

    Args:
        local_dir (str): ローカルのディレクトリパス
        remote_dir (str): リモートの保存先ディレクトリパス
        hostname (str): サーバーのホスト名
        username (str): サーバーのユーザー名
        password (str): サーバーのパスワード
    """
    try:
        # SSHクライアントの設定
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # ホスト鍵を自動で追加
        ssh.connect(hostname, username=username, password=password)

        # SCPクライアントを作成し、ディレクトリを転送
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_dir, remote_dir, recursive=True)  # ディレクトリを再帰的に転送

        print("ディレクトリの転送が成功しました")
    
    except Exception as e:
        print(f"ディレクトリ転送中にエラーが発生しました: {e}")
    finally:
        ssh.close()

# 使用例
if __name__ == "__main__":
    local_dir = "./tmp"
    remote_dir = ""
    hostname = ""
    username = ""
    password = ""

    transfer_directory(local_dir, remote_dir, hostname, username, password)


import time
import google.generativeai as genai

def process_video_and_generate_annotations(video_file_path, api_key, model_name="models/gemini-1.5-pro-latest"):
    """
    動画ファイルをアップロードして、処理が完了したら指定されたモデルでアノテーションを生成します。

    Args:
        video_file_path (str): アップロードする動画ファイルのパス
        api_key (str): Google APIキー
        model_name (str): 使用するモデル名 (デフォルトは"models/gemini-1.5-pro-latest")

    Returns:
        str: 推論結果のテキスト（JSON形式でのアノテーション）
    """
    # Google APIキーの設定
    genai.configure(api_key=api_key)

    # 動画のアップロード
    video_file = genai.upload_file(path=video_file_path)
    print("Completed upload:", video_file.uri)

    # APIがファイルを受信したことを確認し、処理が完了するまで待機
    while video_file.state.name == "PROCESSING":
        print('Waiting for video to be processed.')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)

    # 処理が失敗した場合はエラーを発生させる
    if video_file.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {video_file.state.name}")

    print("Video processing complete:", video_file.uri)

    # モデルの準備
    model = genai.GenerativeModel(model_name=model_name)

    # 推論の実行
    response = model.generate_content(
        [
            "まず、この動画をシーンの切り替わりや映っている動物の切り替わり場面でjson形式でまとめてください。"
            "また、それぞれのシーンについて映っている動物について英語と日本語のアノテーションを複数自動生成してください。"
            "固有名詞は使わないでください。これらをうまくjsonファイルでまとめてください。jsonの形式は次のようにしてください："
            "{"
            "scene: 3,"
            "start_time: 00:29,"
            "end_time: 00:43,"
            "animals: ["
            "{"
            "name_en: [],"
            "name_ja: [],"
            "description_en: [],"
            "description_ja: []"
            "}"
            "]"
            "}、出力はjson形式だけでそれ以外は出力しないでください ",
            video_file
        ],
        request_options={"timeout": 600}  # タイムアウト指定
    )

    # 推論結果（JSON形式のアノテーション）を返
    print(response)
    return response.text

# 使用例
if __name__ == "__main__":
    # 動画ファイルパスとAPIキー
    video_file_path = "./videos/video1.mp4"
    api_key = ""  # TODO: セキュリティのため、envファイルや別途設定で読み込むべき

    # 動画処理とアノテーション生成を実行
    result = process_video_and_generate_annotations(video_file_path, api_key)

    # 結果を表示
    print(result)


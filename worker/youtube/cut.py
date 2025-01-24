import os
import json
from moviepy.editor import VideoFileClip
import paramiko
from scp import SCPClient


def extract_scene(video_file_path, scene_start, scene_end, output_dir, scene_num):
    """
    動画から指定されたシーンを切り出し、指定されたディレクトリに保存します。
    """
    # 動画を読み込む
    clip = VideoFileClip(video_file_path)

    # シーンの開始時間と終了時間を秒で指定
    start_time = scene_start
    end_time = scene_end

    # シーンの切り出し
    scene_clip = clip.subclip(start_time, end_time)

    # 出力ファイル名の設定
    scene_video_path = os.path.join(output_dir, f"scene_{scene_num}.mp4")

    # 切り出したシーンを保存
    scene_clip.write_videofile(scene_video_path, codec='libx264')

    return scene_video_path


def generate_scene_json(scene_data, output_dir, scene_num):
    """
    動物のアノテーションを含むシーン用のJSONファイルを生成します。
    """
    scene_json_path = os.path.join(output_dir, f"scene_{scene_num}.json")

    with open(scene_json_path, 'w', encoding='utf-8') as f:
        json.dump(scene_data, f, ensure_ascii=False, indent=4)

    return scene_json_path


def process_video_and_generate_annotations_cut(video_file_path, json_file_path, output_base_dir):
    """
    動画ファイルとJSONファイルを受け取り、シーンごとに処理を行い、結果のディレクトリを作成します。
    """
    # JSONファイルを読み込む
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_input = json.load(f)

    # 動画ファイルの拡張子と出力先ディレクトリの設定
    video_file_name = os.path.basename(video_file_path)
    output_base_dir = os.path.join(output_base_dir, video_file_name.split('.')[0])

    # 出力先の親ディレクトリを作成
    os.makedirs(output_base_dir, exist_ok=True)

    # JSONを解析してシーンごとに処理
    for scene_num, scene in enumerate(json_input, start=1):
        start_time = scene["start_time"]
        end_time = scene["end_time"]
        animals = scene["animals"]

        # 動画のシーンを切り出し
        scene_output_dir = os.path.join(output_base_dir, f"scene_{scene_num}")
        os.makedirs(scene_output_dir, exist_ok=True)

        scene_video_path = extract_scene(video_file_path, start_time, end_time, scene_output_dir, scene_num)

        # シーンのアノテーションを更新
        scene_data = {
            "scene": scene_num,
            "start_time": start_time,
            "end_time": end_time,
            "animals": animals
        }

        # JSONファイルを生成
        scene_json_path = generate_scene_json(scene_data, scene_output_dir, scene_num)

        # 出力結果のファイルパスを返す
        print(f"Scene {scene_num} processed: Video - {scene_video_path}, JSON - {scene_json_path}")

    print("処理完了！")


# 使用例
if __name__ == "__main__":
    video_file_path = "./videos/video1.mp4"  # 動画ファイルパス
    json_file_path = "./videos/scenes.json"  # JSONファイルパス
    output_base_dir = "./tmp"  # 出力先の親ディレクトリ

    process_video_and_generate_annotations_cut(video_file_path, json_file_path, output_base_dir)


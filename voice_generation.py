import requests
import os
import shutil
import json
import time
import wave

def script_to_act():

    # スクリプトファイルの読み込み
    with open('script.json', 'r', encoding='utf-8') as f:
        script = json.load(f)

    dir_path = "../StreamingAssets/Audio/voice_files"

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)

    os.mkdir(dir_path)

    # キャラクターごとに、Voicevox APIを呼び出して音声を合成する
    for line in script['scripts']:
        # ファイル名に用いるunix時間取得
        ut = time.time()
        
        # タイムスタンプをJSONに追加する
        line["timestamp"] = str(ut)
        
        if line['character'] == 'ずんだもん':
            character_id = 1
        elif line['character'] == '四国めたん':
            character_id = 2
        elif line['character'] == '春日部つむぎ':
            character_id = 8
        else:
            character_id = 1  # デフォルトはずんだもん

        # Voicevox APIにPOSTするデータを作成する
        # audio_query (音声合成用のクエリを作成するAPI)
        res1 = requests.post("http://localhost:50021/audio_query",
                            params={"text": line['line'], "speaker": character_id})

        # synthesis (音声合成するAPI)
        res2 = requests.post("http://localhost:50021/synthesis",
                        params={"speaker": character_id},
                        data=json.dumps(res1.json()))
        
        print("Res2 status code:", res2.status_code)
        

        # 音声ファイルを保存する
        with wave.open(f"{dir_path}/{ut}.wav", 'wb') as f:
            f.setnchannels(1)  # モノラル
            f.setsampwidth(2)  # 16ビット
            f.setframerate(24000)  # サンプリング周波数
            f.writeframes(res2.content)
            
        # 音声ファイルの再生時間を取得する
        with wave.open(f"{dir_path}/{ut}.wav", 'rb') as f:
            duration = f.getnframes() / f.getframerate()

        # script_lineにduration（再生時間）を追加する
        line["duration"] = duration
        
        with open('script.json', 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    script_to_act()
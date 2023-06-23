import os
import shutil
import json
import time
import wave
import logging
from voicevox_core import VoicevoxCore, AccelerationMode

# Loggerの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def script_to_act():
    # Voicevox Coreのインスタンスを作成
    logger.debug("Initializing Voicevox Core")
    core = VoicevoxCore(acceleration_mode=AccelerationMode.AUTO)

    # スクリプトファイルの読み込み
    logger.debug("Loading script.json")
    with open('script.json', 'r', encoding='utf-8') as f:
        script = json.load(f)

    dir_path = "./voice_files"

    if os.path.exists(dir_path):
        logger.debug(f"Removing existing directory: {dir_path}")
        shutil.rmtree(dir_path)

    logger.debug(f"Creating directory: {dir_path}")
    os.mkdir(dir_path)

    # キャラクターごとに、Voicevox Coreを呼び出して音声を合成する
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

        # モデルをロードする
        logger.debug(f"Loading model for character id {character_id}")
        core.load_model(character_id)

        # 音声クエリを作成する
        logger.debug(f"Creating audio query for line: {line['line']}")
        audio_query = core.audio_query(text=line['line'], speaker_id=character_id)

        # 音声合成する
        logger.debug(f"Performing synthesis for character id {character_id}")
        wav = core.synthesis(audio_query, character_id)

        # 音声ファイルを保存する
        logger.debug(f"Saving audio to file: {dir_path}/{ut}.wav")
        with wave.open(f"{dir_path}/{ut}.wav", 'wb') as f:
            f.setnchannels(1)  # モノラル
            f.setsampwidth(2)  # 16ビット
            f.setframerate(24000)  # サンプリング周波数
            f.writeframes(wav)
            
        # 音声ファイルの再生時間を取得する
        with wave.open(f"{dir_path}/{ut}.wav", 'rb') as f:
            duration = f.getnframes() / f.getframerate()

        # script_lineにduration（再生時間）を追加する
        line["duration"] = duration
        logger.debug(f"Duration added to the script line: {duration}")
        
        with open('script.json', 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    script_to_act()

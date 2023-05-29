import os
import json
import openai
import requests
from dotenv import load_dotenv

load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def backscreen_generation():
    # スクリプトファイルの読み込み
    with open('script.json', 'r', encoding='utf-8') as f:
        script = json.load(f)
        
    # バックスクリーンの生成
    response = openai.Image.create(
        prompt=script["dalle_prompt"],
        n=1,
        size="1024x1024",
        response_format="url"
    )
    
    # 画像のURLを取得
    image_url = response['data'][0]['url']

    # 画像をローカルに保存
    image_data = requests.get(image_url).content
    with open("../Images/backscreen.png", "wb") as f:
        f.write(image_data)

if __name__ == "__main__":
    backscreen_generation()

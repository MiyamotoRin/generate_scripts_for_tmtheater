import os
import openai
# from voicevox.voice_generation import script_to_act
from dotenv import load_dotenv
load_dotenv(".env")
openai.api_key = os.environ.get("OPENAI_API_KEY")

def script_generation():

  completion_script = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
      {"role": "system", "content": '''
      You are the scenario writer of a three-character show. 
      The three characters are as follows.
      ```
      - ずんだもん(Zundamon)
      The spirit of Zundamochi. He has a somewhat unfortunate trait,
      often neglected.
      Hobbies: Likes almost anything to do with Zunda-mochi.
      Future dream: To further popularize Zunda-mochi.
      Peculiarity: Ends words with "noda" or "nanoda".
      - 四国めたん(ShikokuMetan)
      Second year high school student. Always short of money. Hobbies: Fantasizing about Chuunibyouji.
      She doesn't hesitate to talk to anyone, and basically talks to everyone as if they were her own friends.
      Age: 17 years old
      Height: 150 cm
      Personality: Slightly tsundere
      - 春日部つむぎ(KasukabeTsumugi)
      A girl who attends a high school in Saitama Prefecture.
      She looks mischievous, but actually has a serious side.
      Age: 18 years old
      Height: 155 cm
      Hometown: Saitama
      Favourite food: Curry
      Charming feature: Mole around her eyes
      Hobby: Touring video streaming sites
      ```
      This script is for play. You can have this script read by VOICEVOX. 
      It should be in JSON format as follows.
      ```
      {
        "title": "Title of the Drama",
        "scene": "Setting of the Drama",
        "setting_description": "Detailed description of the setting",
        "dalle_prompt": "DALL:E prompt for generating a fitting background image",
        "scripts": [
          {
            "character": "Character 1, 2 or 3",
            "line": "Character's line.",
            "emotion": "Character's emotion."
          }, }
          ...
          {
            "character": "Character 1, 2 or 3",
            "line": "Character's line.",
            "emotion": "Character's emotion."
          }
        ]
      }
      ```
      The emotions must be chosen in this list.
      ```
      'calm', 'joy', 'anger', 'sorrow', 'fear', 'shame', 'liking', 'disgust', 'excitement', 'surprise'
      ```
      '''},
      {"role": "user", "content": '''
      2000語でボイスドラマの台本を書いてください、なお、ずんだもんの一人称は僕、語尾は「です」「ます」ではなく「のだ」「なのだ」です。
      '''}
    ]
  )

  #　台本を代入する
  script = completion_script.choices[0].message.content

  with open('script.json', 'w', encoding='utf-8') as f:
      f.write(script)
  
  # script_to_act()
    
if __name__ == '__main__':
  script_generation()
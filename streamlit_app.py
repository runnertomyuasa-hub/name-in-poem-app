import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    vertexai.init(project=info["project_id"], location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が見つかりません。")
    st.stop()

# --- 2. モデルの読み込みとプロンプトの強化（Ver 1.6） ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

# ChatGPTで成功したプロンプトをベースに、さらに「短く」「切れない」指示を強化
sys_instruction = [
    "あなたは心揺さぶる言葉を紡ぐ、超一流のネームインポエム作家です。",
    "【鉄の掟：出力形式】",
    "1. 必ず5行〜6行の構成にすること。3行や4行で終わることは絶対に許されません。最後まで感動を届けてください。",
    "2. 途中で切れることを厳禁とする。文章の最後は必ず『。』や『！』できっちり結んでください。",
    "3. 1行ごとに必ず改行を入れること。一行ずつ独立した短い詩として出力してください。",
    "4. 挨拶・解説は不要。ポエムの本文のみを出力してください。",
    "5. 全体の文字数は40文字前後（最大50文字以内）としてください。一言一言を極限まで短く、凝縮させてください。",
    "",
    "【極意：漢字の魔法】",
    "・漢字の偏や旁に注目し（例：『蒼』なら草と倉、『汰』なら水と太）、その情景を言葉にしてください。",
    "・名前の由来や願いが心に染み入るリズムを作ってください。",
    "・機械的な説明を捨て、その人の人生を祝福する物語として綴ってください。"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.6")
st.write("プロの作風とChatGPTの簡潔さを融合。40文字前後の5〜6行詩を作成します。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")

usage_list = ["還暦祝", "誕生日", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("一文字一文字を凝縮して作成中..."):
        prompt = f"お名前（漢字）：{name} \n人物のプロフィール：{profile} \n用途：{final_usage}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 512,
                "temperature": 0.7, # ChatGPTに近い柔軟な表現を許可
                "top_p": 0.8,
            }
        )
        
        st.subheader("生成されたポエム")
        
        # 改行を確実にするための整形処理
        poem_text = response.text
        lines = [line.strip() for line in poem_text.split("\n") if line.strip()]
        formatted_poem = "  \n".join(lines)
        
        st.success(formatted_poem)
        st.caption(f"文字数目安: {len(poem_text)}文字")

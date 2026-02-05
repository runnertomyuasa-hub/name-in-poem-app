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

# --- 2. モデルの読み込みとプロンプトの強化（Ver 1.4） ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

sys_instruction = [
    "あなたはプロのネームインポエム作家です。必ず以下のルールを厳守して詩を作成してください。",
    "【出力形式の絶対ルール】",
    "1. 行ごとに必ず『2回改行』を入れる: 各行の終わりに空行を入れて、視覚的に1行ずつ独立させてください。",
    "2. 5〜6行で完結させる: 途中で文章を終わらせず、必ず最後の一句まで書ききってください。",
    "3. 漢字の強調: 名前（漢字）やパーツを必ず【 】で囲んでください。",
    "4. 余計な挨拶は禁止: 詩の本文のみを出力してください。",
    "",
    "【表現の極意】",
    "・『小』なら『小さな木片』、『五』なら『五感を研ぎ澄ます』など、漢字の要素から物語を広げてください。",
    "・ひらがなを効果的に混ぜ、リズム感のある優しい口調で綴ってください。"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.4")
st.write("プロの作風を学習したAIが、漢字に魂を込めて5〜6行の詩を綴ります。")

name = st.text_input("お名前（漢字）", "小五郎")
profile = st.text_area("人物のプロフィール", "勇ましい大工さん。ピアノも得意。")

usage_list = ["誕生日", "還暦祝", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("一字一字、心を込めて執筆中..."):
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.5, # 情緒的な広がりを持たせる
            }
        )
        
        st.subheader("生成されたポエム")
        
        # 【改善】AIが改行を忘れても、プログラム側で改行を強制的に見やすく調整します
        poem_text = response.text
        # もし改行が少なければ、。やスペースで改行を促す処理を入れます
        display_text = poem_text.replace("\n", "\n\n") 
        
        st.info(display_text)

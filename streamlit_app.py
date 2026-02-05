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

# --- 2. モデルの読み込みとプロンプトの強化（Ver 1.5） ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

sys_instruction = [
    "あなたは心揺さぶる言葉を紡ぐ、超一流のネームインポエム作家です。",
    "【鉄の掟：出力形式】",
    "1. 必ず5行〜6行の構成にすること: 3行や4行で終わることは絶対に許されません。最後まで感動を届けてください。",
    "2. 途中で切れることを厳禁とする: 文章の最後は必ず『。』や『！』、あるいは余韻を残す言葉できっちり結んでください。",
    "3. 1行ごとに改行を入れる: 読点（、）で繋がず、1行ずつ独立した詩として出力してください。",
    "4. 挨拶・解説は不要: ポエムの本文のみを出力してください。",
    "",
    "【極意：漢字の魔法】",
    "・漢字の偏や旁に注目し（例：『蒼』なら草と倉、『汰』なら水と太）、その情景を詩に織り込んでください。",
    "・『読み』のひらがなを優しく混ぜ、名前の由来や願いが心に染み入るリズムを作ってください。",
    "・機械的な説明を捨て、その人の人生を祝福する物語として綴ってください。"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.5")
st.write("プロの作風を学習したAIが、漢字の奥深さを活かして、最後まで丁寧に詩を書き上げます。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "蒼い空のように広い心。たくましい子に育ってほしい。")

usage_list = ["誕生日", "還暦祝", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("一字一字に魂を込め、最後まで書き上げ中..."):
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.6, # 情緒的な『ゆらぎ』と『深み』を出すために微増
                "top_p": 0.95,
            }
        )
        
        st.subheader("生成されたポエム")
        
        # 【修正】Markdownのルール（末尾の半角スペース2つ）を適用して、確実に改行させます
        poem_text = response.text
        lines = poem_text.split("\n")
        # 各行の末尾に半角スペース2つを付与して改行を保証
        formatted_poem = "  \n".join([line.strip() for line in lines if line.strip()])
        
        st.info(formatted_poem)

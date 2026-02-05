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

# --- 2. モデルの読み込みとプロンプトの強化（Ver 1.7） ---
# 先ほどデプロイした最新のエンドポイントIDを反映しています
model_path = "projects/180827076471/locations/us-central1/endpoints/394835391592010432"

# 10枚の色紙学習(v2)を活かしつつ、ChatGPTで成功した「40文字・短文」を死守する指示
sys_instruction = [
    "あなたは心揺さぶる言葉を短く凝縮して紡ぐ、超一流のネームインポエム作家です。",
    "【出力形式の鉄則】",
    "1. 必ず「5行から6行」で構成してください。1行を極限まで短くすること。",
    "2. 文章の最後は必ず『。』や『！』できっちり結び、途中で切れることを厳禁とします。",
    "3. 全体の文字数は「40文字前後」に抑えてください（最大50文字）。",
    "4. 名前（漢字）やその一部を必ず【 】で囲んで組み込んでください。",
    "5. 挨拶や解説、導入文は一切出力せず、ポエムの本文のみを表示してください。",
    "",
    "【表現の極意】",
    "・学習データ(v2)の作風をベースに、漢字の偏や旁から豊かな情景を連想してください。",
    "・リズム感を大切にし、ひらがなを優しく交えて、人生を祝福する物語を綴ってください。"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.7")
st.write("最新の学習モデル(v2)を搭載。一文字一文字に魂を込めた40文字の詩を贈ります。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")

# 用途の選択
usage_list = ["還暦祝", "誕生日", "古希祝", "誕生・命名祝い", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("最新の学習成果を呼び出し中..."):
        # プロンプトの形式を学習データに合わせます
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 512,
                "temperature": 0.7, # 表現の幅を持たせつつ、学習結果を反映
                "top_p": 0.8,
            }
        )
        
        st.subheader("生成されたポエム")
        
        # Markdownの改行ルール（行末スペース2つ）を適用して、確実に改行を表示
        poem_text = response.text
        lines = [line.strip() for line in poem_text.split("\n") if line.strip()]
        formatted_poem = "  \n".join(lines)
        
        st.success(formatted_poem)
        st.caption(f"（生成文字数: {len(poem_text.replace(' ', '').replace('\\n', ''))}文字 / モデル: name_in_poem_v2）")

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

# --- 2. モデルの読み込み ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"
model = GenerativeModel(model_path)

# --- 3. 画面デザイン ---
# タイトルをご要望通りに変更
st.title("🌸 名前でポエム！")
st.write("プロの作風を学習したAIが、お名前に合わせた5〜6行の詩を作成します。")

name = st.text_input("お名前（漢字）", "小五郎")
profile = st.text_area("人物のプロフィール（性格や趣味など）", "勇ましい大工さん。ピアノも得意。")

# 用途の選択肢を細分化（ご要望通りに変更）
usage_list = ["誕生日", "還暦祝", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("プロの作風を再現中..."):
        # 【最重要】学習データ(JSONL)と一文字も違わない形式でプロンプトを作成します
        # これにより、AIが「あの学習したパターンだ！」と即座に理解します
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        # temperatureを0.0に設定し、学習したパターンから「一歩も外れない」ように固定します
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 512,
                "temperature": 0.0, 
                "top_p": 0.95
            }
        )
        
        st.subheader("生成されたポエム")
        # 詩を見やすく枠で囲んで表示します
        st.success(response.text)

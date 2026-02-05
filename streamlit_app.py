import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 金庫（Secrets）から鍵を取り出す設定 ---
if "gcp_service_account" in st.secrets:
    # Secretsに貼り付けた情報を読み込む
    info = st.secrets["gcp_service_account"]
    # Google Cloudが理解できる形式に変換
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # 認証情報を使ってVertex AIを初期化
    vertexai.init(
        project=info["project_id"],
        location="us-central1",
        credentials=credentials
    )
else:
    st.error("Secretsの設定（gcp_service_account）が見つかりません。")
    st.stop()

# --- 2. モデルの準備 ---
# あなたの正しいエンドポイント住所を指定
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"
model = GenerativeModel(model_path)

# --- 3. アプリの画面構成（Streamlit） ---
st.title("🌸 ネームインポエム作成")
st.write("大切なお名前で、世界に一つの詩を贈ります。")

name = st.text_input("お名前（漢字）", "陽葵")
profile = st.text_area("人物のプロフィール", "向日葵のように明るい笑顔の女の子")
usage = st.selectbox("用途", ["初節句のお祝い", "お誕生日", "結婚祝い", "還暦祝い"])

if st.button("詩を作成する"):
    with st.spinner("AIが学習した作風で詩を考えています..."):
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{usage}"
        response = model.generate_content(prompt)
        
        st.subheader("生成されたポエム")
        st.success(response.text)

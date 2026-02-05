import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account
import json
import os

# ページ設定
st.set_page_config(
    page_title="ネームインポエム作成",
    page_icon="🌸",
    layout="centered"
)

# Vertex AI設定 (ハードコーディング)
PROJECT_ID = "180827076471"
LOCATION = "us-central1"
ENDPOINT_ID = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

# 初期化関数（キャッシュして高速化）
@st.cache_resource
def load_model():
    # Streamlit CloudのSecretsから認証情報を読み込む場合
    if "gcp_service_account" in st.secrets:
        # st.secretsはTOML形式だが辞書として扱える
        creds_info = dict(st.secrets["gcp_service_account"])
        
        # private_keyの改行コード変換（TOMLの制約対策）
        if "private_key" in creds_info:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
            
        creds = service_account.Credentials.from_service_account_info(creds_info)
        vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=creds)
    else:
        # ローカル実行（gcloud auth application-default login済み）の場合
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        
    return GenerativeModel(ENDPOINT_ID)

# UIヘッダー
st.title("🌸 ネームインポエム作成")
st.markdown("大切な人のお名前で、世界に一つの詩を贈ります。")

# 入力フォーム
with st.form("poem_form"):
    kanji = st.text_input("お名前（漢字）", placeholder="例：陽葵")
    
    profile = st.text_area("人物のプロフィール", 
                         placeholder="例：向日葵のように明るい笑顔の女の子。4月から小学生。",
                         height=100)
    
    purpose = st.selectbox("用途", 
                         ["お祝い", "プレゼント", "記念日", "感謝", "その他"])
    
    submitted = st.form_submit_button("詩を作成する", type="primary")

# 生成ロジック
if submitted:
    if not kanji or not profile:
        st.error("お名前とプロフィールを入力してください。")
    else:
        try:
            with st.spinner('AIが詩を考案中です...'):
                model = load_model()
                prompt = f"漢字：{kanji}、プロフィール：{profile}、用途：{purpose}"
                response = model.generate_content(prompt)
                
            st.success("作成しました！")
            st.markdown("---")
            st.subheader("📝 生成された詩")
            st.write(response.text)
            st.markdown("---")
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.info("※Google Cloudの認証設定が必要です（ローカル実行時）。")

# フッター
st.markdown("---")
st.caption("Powered by Google Vertex AI (Fine-tuned Model)")

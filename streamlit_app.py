import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # プロジェクト番号(180827076471)で初期化
    vertexai.init(project="180827076471", location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（正解：モデルIDを使用） ---
# 画像016.jpgのURLから抽出した、特訓済みモデル本体のIDです
model_id = "1362918329907412992" 
model_path = f"projects/180827076471/locations/us-central1/models/{model_id}"

sys_instruction = ["あなたはプロのポエム作家です。40文字前後の5〜6行詩を、改行を多用して作成してください。"]

try:
    # 権限さえあれば、この「モデルパス」で確実に読み込めます
    model = GenerativeModel(model_name=model_path, system_instruction=sys_instruction)
except Exception as e:
    st.error(f"モデルの準備に失敗しました: {e}")

# --- 3. メイン画面 ---
st.title("🌸 名前でポエム！ Ver 2.6")
st.write("ついに開通。特訓の成果を今、あなたに。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("プロフィール", "明るい。ピアノが得意。")

if st.button("詩を作成する"):
    with st.spinner("AIが特訓の成果を絞り出しています..."):
        try:
            prompt = f"漢字：{name}、プロフィール：{profile}"
            response = model.generate_content(prompt)
            st.success(response.text.replace("\n", "  \n"))
        except Exception as e:
            st.error("生成中にエラーが発生しました。")
            st.code(f"診断情報:\nPath: {model_path}\nError: {e}")

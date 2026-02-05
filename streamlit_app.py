import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # 確実にプロジェクト番号(180827076471)で初期化します
    PROJECT_NUMBER = "180827076471"
    vertexai.init(project=PROJECT_NUMBER, location="us-central1", credentials=credentials)
else:
    st.error("Secretsが見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（Ver 2.2） ---
# パスに「名前」ではなく「数字」を直接埋め込みます
endpoint_id = "394835391592010432"
model_path = f"projects/180827076471/locations/us-central1/endpoints/{endpoint_id}"

sys_instruction = ["あなたはプロのポエム作家です。40文字前後の5〜6行詩を作成してください。"]

try:
    model = GenerativeModel(model_name=model_path, system_instruction=sys_instruction)
except Exception as e:
    st.error(f"初期化エラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 2.2")
st.sidebar.write(f"接続先プロジェクト番号: 180827076471")
st.sidebar.write(f"使用エンドポイントID: {endpoint_id}")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("AIが言葉を紡いでいます..."):
        try:
            prompt = f"漢字：{name}、プロフィール：{profile}"
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 512, "temperature": 0.7}
            )
            
            st.subheader("生成されたポエム")
            # 改行を確実に反映
            st.success(response.text.replace("\n", "  \n"))
            
        except Exception as e:
            st.error("生成に失敗しました。")
            # エラーの詳細をそのまま表示
            st.code(f"【デバッグ情報】\n使用パス: {model_path}\nエラー内容: {e}")

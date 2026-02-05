import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # Secretsから読み取ったプロジェクトIDをそのまま使用
    target_project = info["project_id"]
    vertexai.init(project=target_project, location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が見つかりません。Streamlit管理画面のSecretsを確認してください。")
    st.stop()

# --- 2. モデルの読み込み（Ver 2.1） ---
# 最新のID「394835391592010432」を確実に指定
endpoint_id = "394835391592010432"
model_path = f"projects/{target_project}/locations/us-central1/endpoints/{endpoint_id}"

sys_instruction = [
    "あなたはプロのネームインポエム作家です。",
    "40文字前後の5〜6行詩を作成してください。",
    "【重要】必ず改行を含めてください。"
]

try:
    model = GenerativeModel(
        model_name=model_path,
        system_instruction=sys_instruction
    )
except Exception as e:
    st.error(f"モデル接続エラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 2.1")
# サイドバーに現在の設定を表示して確認できるようにします
with st.sidebar:
    st.write("### 接続ステータス")
    st.info(f"プロジェクト: {target_project}")
    st.info(f"エンドポイント末尾: ...{endpoint_id[-4:]}")

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
            
            # 結果表示（改行を反映）
            st.subheader("生成されたポエム")
            st.success(response.text.replace("\n", "  \n"))
            
        except Exception as e:
            st.error("生成中にエラーが発生しました。")
            st.code(f"診断用エラーメッセージ:\n{e}")

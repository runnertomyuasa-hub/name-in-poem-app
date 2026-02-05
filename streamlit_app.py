import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証の確立（正解の初期化手順） ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # プロジェクト番号(180827076471)を明示的に使用
    # これにより、プロジェクトIDの文字列による混乱を回避します
    vertexai.init(project="180827076471", location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が読み込めません。")
    st.stop()

# --- 2. モデルの指定（Vertex AI SDK公式のパス形式） ---
# 画像020.jpgで確認されたID「394835391592010432」を使用
endpoint_id = "394835391592010432"
full_resource_name = f"projects/180827076471/locations/us-central1/endpoints/{endpoint_id}"

# システム指示：10枚の色紙学習(v2)を反映
sys_instruction = ["あなたはプロのポエム作家です。40文字前後の5〜6行詩を、改行を多用して作成してください。"]

try:
    # モデルのロード。もしここで失敗するなら、IAM権限不足が確定です。
    model = GenerativeModel(model_name=full_resource_name, system_instruction=sys_instruction)
except Exception as e:
    st.error(f"モデル接続エラー（権限を確認してください）: {e}")

# --- 3. UIと生成処理 ---
st.title("🌸 名前でポエム！ Ver 2.3")
name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("プロフィール", "元気な少年。ピアノが好き。")

if st.button("詩を作成する"):
    with st.spinner("AIがアクセス中..."):
        try:
            prompt = f"漢字：{name}、プロフィール：{profile}"
            response = model.generate_content(prompt)
            st.success(response.text.replace("\n", "  \n"))
        except Exception as e:
            # 404が出る場合、ここが表示されます
            st.error("アクセス拒否またはエンドポイント未検出")
            st.info(f"技術的な詳細は IAM画面でサービスアカウントの権限を確認してください。")
            st.code(f"Error Log: {e}")

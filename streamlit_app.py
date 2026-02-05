import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # 診断用：Secretsに設定されているプロジェクトIDを表示（後で削除してください）
    # st.sidebar.write(f"認証中のプロジェクト: {info['project_id']}")
    
    vertexai.init(project=info["project_id"], location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（Ver 1.8） ---
# 数字の番号ではなく、プロジェクト名「name-in-poem」を直接使う形式に変更します
# これにより、プロジェクトIDの取り違えを確実に防ぎます
model_path = "projects/name-in-poem/locations/us-central1/endpoints/394835391592010432"

sys_instruction = [
    "あなたはプロのネームインポエム作家です。学習データ(v2)の作風を守り、40文字前後の5〜6行詩を作成してください。",
    "【鉄則】必ず5〜6行で改行し、途中で切らずに『！』や『。』で結んでください。"
]

# モデルの読み込みをtry-exceptで囲み、エラーの内容を詳細に表示させます
try:
    model = GenerativeModel(
        model_name=model_path,
        system_instruction=sys_instruction
    )
except Exception as e:
    st.error(f"モデルの読み込みに失敗しました。パスが正しいか確認してください。\nエラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.8")
st.write("最新の学習モデル(v2)で、心に響く詩を最後まで綴ります。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")
usage_choice = st.selectbox("用途", ["還暦祝", "誕生日", "古希祝", "誕生・命名祝い", "その他"])

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("最新のAIが執筆中..."):
        try:
            prompt = f"漢字：{name}、プロフィール：{profile}、用途：{usage_choice}"
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 512, "temperature": 0.7}
            )
            
            st.subheader("生成されたポエム")
            # 改行を確実に反映
            formatted_poem = "  \n".join([l.strip() for l in response.text.split("\n") if l.strip()])
            st.success(formatted_poem)
            
        except Exception as e:
            st.error("生成中にエラーが発生しました。")
            st.info(f"技術的な詳細: {e}")

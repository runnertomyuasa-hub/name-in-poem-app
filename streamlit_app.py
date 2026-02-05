import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # 画像021.jpgで確認した正しいプロジェクト名で初期化
    vertexai.init(project="name-in-poem", location="us-central1", credentials=credentials)
else:
    st.error("Secretsが見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（画像023.jpgの最新IDを反映） ---
# 確実に 9172529519674785792 を設定しました
endpoint_id = "9172529519674785792"
model_path = f"projects/name-in-poem/locations/us-central1/endpoints/{endpoint_id}"

# 特訓済みモデル(v2)の魂を込めた指示
sys_instruction = [
    "あなたは超一流のネームインポエム作家です。",
    "【出力形式の鉄則】",
    "1. 必ず「5行から6行」で構成してください。",
    "2. 文章の最後は必ず『。』や『！』できっちり結び、途中で切らないこと。",
    "3. 全体の文字数は「40文字前後」に抑えてください。",
    "4. 名前（漢字）を必ず【 】で囲んで組み込んでください。",
    "5. 挨拶や解説は一切出力せず、ポエムのみを表示してください。"
]

try:
    # 新しいエンドポイントに接続
    model = GenerativeModel(
        model_name=model_path,
        system_instruction=sys_instruction
    )
except Exception as e:
    st.error(f"モデル接続エラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 2.9")
st.write("最新の学習成果(v2)を搭載。一文字一文字に魂を込めた詩を贈ります。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")

# 用途の選択
usage_choice = st.selectbox("用途", ["還暦祝", "誕生日", "古希祝", "誕生・命名祝い", "退職祝い", "結婚祝い", "その他"])

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("新しいエンドポイントへアクセス中..."):
        try:
            # 学習データに基づいたプロンプト
            prompt = f"漢字：{name}、プロフィール：{profile}、用途：{usage_choice}"
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 512,
                    "temperature": 0.7,
                }
            )
            
            st.subheader("生成されたポエム")
            # 改行を確実に反映して表示
            formatted_poem = response.text.replace("\n", "  \n")
            st.success(formatted_poem)
            
        except Exception as e:
            st.error("生成中にエラーが発生しました。")
            st.code(f"技術詳細: {e}")

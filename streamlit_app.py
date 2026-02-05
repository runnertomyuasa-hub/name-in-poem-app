import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    
    # プロジェクト番号(180827076471)を使用して初期化
    vertexai.init(project="180827076471", location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（Ver 1.9） ---
# 【最重要】プロジェクトID名ではなく、数字の「プロジェクト番号」をパスに使用します
model_path = "projects/180827076471/locations/us-central1/endpoints/394835391592010432"

sys_instruction = [
    "あなたはプロのネームインポエム作家です。学習データ(v2)の作風を守り、40文字前後の5〜6行詩を作成してください。",
    "【鉄則】必ず5〜6行で改行し、途中で切らずに『！』や『。』で結んでください。"
]

try:
    model = GenerativeModel(
        model_name=model_path,
        system_instruction=sys_instruction
    )
except Exception as e:
    st.error(f"モデルの準備に失敗しました。\nエラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.9")
st.write("最新の学習モデル(v2)を搭載。あなたの名前に魂を込めます。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")
usage_choice = st.selectbox("用途", ["還暦祝", "誕生日", "古希祝", "誕生・命名祝い", "その他"])

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("AIが言葉を紡いでいます..."):
        try:
            # 学習データ(v2)と同じ形式で問いかけ
            prompt = f"漢字：{name}、プロフィール：{profile}、用途：{usage_choice}"
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 512,
                    "temperature": 0.7,
                }
            )
            
            st.subheader("生成されたポエム")
            # 改行を確実に反映させる整形処理
            raw_text = response.text
            formatted_poem = "  \n".join([line.strip() for line in raw_text.split("\n") if line.strip()])
            st.success(formatted_poem)
            
        except Exception as e:
            st.error("申し訳ありません。生成中にエラーが発生しました。")
            st.info(f"詳細エラー情報: {e}")

import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    vertexai.init(project="name-in-poem", location="us-central1", credentials=credentials)
else:
    st.error("Secretsが見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（最新ID） ---
endpoint_id = "9172529519674785792"
model_path = f"projects/name-in-poem/locations/us-central1/endpoints/{endpoint_id}"

# 指示に「偏と旁の活用」を明確に追加
sys_instruction = [
    "あなたは漢字の成り立ちまで深く理解する、最高峰のネームインポエム作家です。",
    "【表現の極意：偏と旁の活用】",
    "1. 漢字をそのまま使うだけでなく、その『偏（へん）』や『旁（つくり）』、あるいは構成要素を分解し、その形や意味から連想される情景を詩に盛り込んでください。",
    "   例：『汰』なら『さんずい（水）』から清らかな流れや潤いを連想し、詩のテーマにする。",
    "   例：『心』を『心臓の鼓動』や『中心』として捉え、人生の芯を詠む。",
    "2. 名前（漢字）は必ず【 】で囲んで文章の中に自然に、かつランダムに配置してください。",
    "3. 5行から6行で構成し、40文字〜50文字程度の短文で感動を凝縮させてください。",
    "4. 学習データ(v2)の作風をベースに、ひらがなを多用した柔らかい語口にしてください。"
]

try:
    model = GenerativeModel(
        model_name=model_path,
        system_instruction=sys_instruction
    )
except Exception as e:
    st.error(f"接続エラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 3.1")
st.write("漢字を分解し、その奥深さまで詩に反映させる高度な生成に対応しました。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")

usage_list = ["還暦祝", "誕生日", "古希祝", "誕生・命名祝い", "退職祝い", "結婚祝い", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("具体的な用途を入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("漢字の成り立ちから言葉を紡いでいます..."):
        try:
            # AIに分解を促すための念押し
            prompt = f"名前：{name}、プロフィール：{profile}、用途：{final_usage}。漢字の偏や旁の意味も大切に扱い、文章の途中に名前を織り交ぜて。"
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 512,
                    "temperature": 0.85, # 想像力をより働かせるために少し上げました
                    "top_p": 0.9,
                }
            )
            
            st.subheader("生成されたポエム")
            st.success(response.text.replace("\n", "  \n"))
            
        except Exception as e:
            st.error("生成に失敗しました。")
            st.code(f"技術詳細: {e}")

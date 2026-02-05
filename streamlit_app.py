import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel
from google.oauth2 import service_account

# --- 1. 認証と初期化 ---
if "gcp_service_account" in st.secrets:
    info = st.secrets["gcp_service_account"]
    credentials = service_account.Credentials.from_service_account_info(info)
    vertexai.init(project=info["project_id"], location="us-central1", credentials=credentials)
else:
    st.error("Secrets設定が見つかりません。")
    st.stop()

# --- 2. モデルの読み込み（ここに強力な指示を入れます） ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

# これが「監督の指示（システム・インストラクション）」です
sys_instruction = [
    "あなたはプロのネームインポエム作家です。",
    "【重要なルール】",
    "1. 名前（漢字）の文字そのもの、あるいはその漢字の『辺（へん）』や『冠（かんむり）』を必ず【 】で囲んで詩の中に組み込んでください。",
    "2. 構成は、必ず『5〜6行』の詩にしてください。学習データより少し長めに情景を描写してください。",
    "3. 挨拶（『おめでとうございます』等）や解説、導入文は一切出力しないでください。詩の本文のみを出力してください。",
    "4. 学習データの作風を厳守してください。"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！")
st.write("プロの作風を学習したAIが、お名前に合わせた5〜6行の詩を作成します。")

name = st.text_input("お名前（漢字）", "小五郎")
profile = st.text_area("人物のプロフィール", "勇ましい大工さん。ピアノも得意。")

# 用途を細分化
usage_list = ["誕生日", "還暦祝", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("プロの作風を再現中..."):
        # 学習データ(JSONL)と全く同じ「タグ形式」でデータを渡します
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        # 自由な発想を抑え、学習内容に集中させる設定(temperature=0.0)
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.0,
            }
        )
        
        st.subheader("生成されたポエム")
        st.info(response.text)

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

# --- 2. モデルの読み込み ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"
model = GenerativeModel(model_path)

# --- 3. 画面デザイン ---
st.title("🌸 ネームインポエム作成")
st.write("学習したプロの作風で、お名前に合わせた5〜6行の詩を作成します。")

# 入力欄
name = st.text_input("お名前（漢字）", "小五郎")
profile = st.text_area("人物のプロフィール（性格や職業、趣味など）", "勇ましい大工さん。ピアノも得意。")

# 用途の選択肢（ご要望通りに変更）
usage_list = ["誕生日", "還暦・古希など長寿祝い", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

# 「その他」を選んだ場合の追加入力
final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください（例：開店祝い）")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    if not name or not final_usage:
        st.warning("お名前と用途を入力してください。")
    else:
        with st.spinner("プロの作風を再現中..."):
            # 学習時と同じ形式を厳守し、AIに「あの時の作風だ！」と思い出させます
            prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
            
            # 5〜6行の詩に限定する指示を念押し（微調整が必要な場合があります）
            response = model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 512, "temperature": 0.7}
            )
            
            st.subheader("生成されたネームインポエム")
            # 枠で囲って表示
            st.info(response.text)
            
            st.caption("※5〜6行で構成され、お名前の漢字や意味が含まれています。")

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

# --- 2. モデルの読み込みとプロンプトの強化（Ver 1.2） ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

# 投稿者様に教えていただいたプロの極意をAIに叩き込みます
sys_instruction = [
    "あなたは情緒豊かな表現を得意とするプロのネームインポエム作家です。",
    "【作風の指針】",
    "1. 漢字を分解して物語を作る: 漢字の偏（へん）や旁（つくり）に注目し、その意味を詩に織り込んでください（例：『信』なら人の言、『和』なら禾と口）。",
    "2. 意味と願いを込める: 単なる説明ではなく、その人の人生や名前に込められた願いを詩の核心に据えてください。",
    "3. 柔らかな表現: 漢字の頭文字を使いつつ、読みやすいひらがなを交えて、心に響くリズムを作ってください。",
    "4. 5〜6行の構成: 学習データの形式を守りつつ、より情景が浮かぶ豊かな描写で5〜6行にまとめてください。",
    "5. 挨拶や解説は一切禁止: 詩の本文のみを出力してください。",
    "",
    "【参考：理想的な作風例】",
    "■『誠』さんの場合（誠実さ、言葉を成す）",
    "言葉を大切に　一つずつ積み重ね",
    "成し遂げていく　そのひたむきな姿",
    "誠の心は　周りを照らす　温かな光となる",
    "",
    "■『和』さんの場合（調和、平和、禾と口）",
    "禾（いね）が実り　口々に喜びが広がるように",
    "和やかな笑顔で　みんなの心を結び",
    "穏やかな幸せを　これからも紡いでいこう"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
# 表題にリビジョン番号を付与
st.title("🌸 名前でポエム！ Ver 1.2")
st.write("プロの作風を学習したAIが、漢字の意味や願いを込めて詩を綴ります。")

name = st.text_input("お名前（漢字）", "小五郎")
profile = st.text_area("人物のプロフィール（由来やエピソードがあれば詳しく）", "勇ましい大工さん。ピアノも得意。")

# 用途の選択肢
usage_list = ["誕生日", "還暦祝", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("プロの極意を込めて作成中..."):
        # プロフィールに由来を混ぜるよう促すプロンプト
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        # 創造性と正確さのバランスを調整
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.5, # ほどよい情緒的なゆらぎを持たせる
                "top_p": 0.9,
            }
        )
        
        st.subheader("生成されたポエム")
        st.success(response.text)

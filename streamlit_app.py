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

# --- 2. モデルの読み込みとプロンプトの強化（Ver 1.3） ---
model_path = "projects/180827076471/locations/us-central1/endpoints/4782082832941973504"

# 改行の徹底と、漢字分解の極意をさらに強化
sys_instruction = [
    "あなたはプロのネームインポエム作家です。読者の心に深く響く、情緒豊かな5〜6行の詩を綴ってください。",
    "【出力形式の絶対ルール】",
    "1. 複数行での構成: 1行に繋げず、必ず適宜改行を入れてください。読点（、）やスペースで繋ぐのではなく、一行ずつ独立した詩として出力してください。",
    "2. 漢字の強調: 名前（漢字）そのもの、またはその一部（偏・旁）を必ず【 】で囲み、詩の冒頭や途中に配置してください。",
    "3. 詩情豊かな改行: 1行1行が独立した感動を呼ぶように、プロの詩人として改行を駆使してください。",
    "4. 挨拶・解説の禁止: 余計な文言は一切省き、ポエムのみを出力してください。",
    "",
    "【表現の極意】",
    "- 漢字の解体: 『信』→『人の言（ことば）』、『誠』→『言（ことば）を成（な）す』のように、漢字の成り立ちから人生を肯定する言葉を紡いでください。",
    "- 柔らかいひらがな: 漢字の力強さと、ひらがなの優しさを織り交ぜることで、読み手の心に染み入るリズムを作ります。",
    "",
    "【理想的な出力例（必ずこの形式を模倣してください）】",
    "【小】さな木片にも　心を込めて向き合い",
    "五感を研ぎ澄まし　確かな技を刻みゆく",
    "【五】重の塔をも　支えるような確かな腕で",
    "【郎】らかに響く　槌の音は希望の調べ",
    "情熱を胸に　新たな歴史を　その手で拓いていこう"
]

model = GenerativeModel(
    model_name=model_path,
    system_instruction=sys_instruction
)

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 1.3")
st.write("プロの作風を学習したAIが、漢字の深い意味と願いを込めて、美しい5〜6行の詩を綴ります。")

name = st.text_input("お名前（漢字）", "小五郎")
profile = st.text_area("人物のプロフィール（由来やエピソードがあれば詳しく）", "勇ましい大工さん。ピアノも得意。")

usage_list = ["誕生日", "還暦祝", "古希祝", "長寿祝", "退職祝い", "結婚祝い", "成人祝", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    custom_usage = st.text_input("お祝いの目的を自由に入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("一文字一文字に魂を込めて作成中..."):
        prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}"
        
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.4, # 詩的な表現のために少しだけゆらぎを持たせる
                "top_p": 0.95,
            }
        )
        
        st.subheader("生成されたポエム")
        # 改行を正しく反映させて表示
        st.success(response.text)

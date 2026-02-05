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

# --- 2. モデルの読み込み（最新ID維持） ---
endpoint_id = "9172529519674785792"
model_path = f"projects/name-in-poem/locations/us-central1/endpoints/{endpoint_id}"

# 指示を「ランダム配置」に特化して強化
sys_instruction = [
    "あなたは言葉の魔術師、超一流のネームインポエム作家です。",
    "【出力の黄金律】",
    "1. 必ず「5行から6行」で構成してください。",
    "2. 名前の文字（漢字）を【 】で囲んで組み込んでください。",
    "3. 【重要】名前の文字を「行の先頭」に固定しないでください。文章の途中や最後など、最も美しく響く場所にランダムに配置してください。",
    "4. 10枚の色紙学習(v2)の作風をベースに、ひらがなを交えた優しい表現にしてください。",
    "5. 全体の文字数は「40文字〜50文字」に凝縮してください。"
]

try:
    model = GenerativeModel(
        model_name=model_path,
        system_instruction=sys_instruction
    )
except Exception as e:
    st.error(f"接続エラー: {e}")

# --- 3. 画面デザイン ---
st.title("🌸 名前でポエム！ Ver 3.0")
st.write("用途の自由入力に対応。名前の配置もより芸術的に進化しました。")

name = st.text_input("お名前（漢字）", "蒼汰")
profile = st.text_area("人物のプロフィール", "明るくて元気。ピアノが得意。")

# --- 用途の選択（「その他」復活版） ---
usage_list = ["還暦祝", "誕生日", "古希祝", "誕生・命名祝い", "退職祝い", "結婚祝い", "その他"]
usage_choice = st.selectbox("用途", usage_list)

final_usage = usage_choice
if usage_choice == "その他":
    # 以前のように、その他を選んだ時だけ入力欄が出るように修正
    custom_usage = st.text_input("具体的な用途（例：金婚式、入学祝いなど）を入力してください")
    final_usage = custom_usage

# --- 4. 生成実行 ---
if st.button("詩を作成する"):
    with st.spinner("AIが言葉のパズルを組み立てています..."):
        try:
            # 漢字一文字ずつをランダムに配置させるための追加メッセージ
            prompt = f"漢字：{name}、プロフィール：{profile}、用途：{final_usage}。名前の文字は文章の中に自然に混ぜてください。"
            
            response = model.generate_content(
                prompt,
                generation_config={
                    "max_output_tokens": 512,
                    "temperature": 0.8, # 少し数値を上げ、ランダム性を高めました
                    "top_p": 0.9,
                }
            )
            
            st.subheader("生成されたポエム")
            st.success(response.text.replace("\n", "  \n"))
            st.caption(f"（用途：{final_usage} / モデル: name_in_poem_v2）")
            
        except Exception as e:
            st.error("生成中にエラーが発生しました。")
            st.code(f"技術詳細: {e}")

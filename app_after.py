# =========================================
# 20251123構築 → VSCode対応 Error改修20251206
# =========================================

import os

# 20251206 Streamlit対応追加
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# ============================
# API Key設定（dotenvに変更）
# ============================
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ============================
# 専門家別 system prompt（最新改定版）
# ============================
expert_prompts = {
    "健康アドバイザー": (
        "あなたは健康に関する専門家です。"
        "エビデンスに基づいた安全なアドバイスを中心に回答してください。"
        "食品・薬・サプリメントに関する内容は、一般的情報の範囲に限定し、"
        "医療行為に該当しないよう注意してください。"
        "回答は箇条書きで、3つ以内にまとめて下さい。"
    ),
    "ITコンサルタント": (
        "あなたはITコンサルタントです。"
        "業務改善につながる実用的な助言を提供してください。"
        "特に、ツール例・費用対効果・実行ステップがわかる形にしてください。"
        "回答は短く、箇条書きを用いて簡潔に提示してください。"
    ),
}

# =========================================
# Streamlit UI（ipywidgets → Streamlitへ置換）
# =========================================
st.title("🎓 専門家チャット AI")

# ▼ ラジオボタン UI 置換版
expert = st.radio("専門家:", list(expert_prompts.keys()))

# ▼ 質問入力 置換版
question = st.text_input("質問:", placeholder="質問を入力してください")

# ▼ 状態表示領域 置換版
status_label = st.empty()
output = st.empty()

# ▼ 送信ボタン処理（on_click → if st.button）
if st.button("送信"):
    if not question:
        st.warning("⚠ 質問を入力してください")
    else:
        status_label.info("⏳ 回答生成中です。しばらくお待ちください...")

        try:
            messages = [
                {"role": "system", "content": expert_prompts[expert]},
                {"role": "user", "content": question},
            ]

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.5,
                messages=messages,
            )

            response = completion.choices[0].message.content

            status_label.success(f"▼ 選択した専門家: {expert}")
            output.write(response)

        except Exception as e:
            st.error(f"⚠ エラーが発生しました: {e}")
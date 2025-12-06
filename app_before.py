# 20251123構築 -> Error改修20251206

# ===================
# 20251204追加及び改定
# ===================
import os
#from google.colab import userdata

from openai import OpenAI
#import ipywidgets as widgets
#from IPython.display import display, clear_output

#20251206追加
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ▼ API Key設定 -> Colab userdata　->ipywidgets依存版
#os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
#client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ▼ 専門家別 system prompt（2人版）
expert_prompts = {
    "健康アドバイザー": "あなたは健康に関する専門家です。エビデンスに基づいた安全なアドバイスをしてください。",
    "ITコンサルタント": "あなたはITコンサルタントです。利用者の業務効率化につながる実用的な助言を提供してください。",
}

# ===================
# 改定案 20251123
# ===================
# ▼ 専門家別 system prompt（2人版）
#expert_prompts = {
#    "健康アドバイザー": "あなたは健康に関する専門家です。エビデンスに基づいた安全なアドバイスをしてください。",
#    "ITコンサルタント": "あなたはITコンサルタントです。業務改善につながる実用的な助言を提供してください。",
#}

#===================
# 改定案　20251206
#===================
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

# ===================
# Streamlit UI開始 -> ipywidgets版
# 以下機能がすべて ipywidgets 依存であるため、
# streamlit環境で動作するコードに変更する。
# ===================

# 修正する機能一覧　20251206
# widgets.RadioButtons
# widgets.Text
# widgets.Button
# widgets.Label
# widgets.Output


# ▼ ラジオボタン UI
#expert_radio = widgets.RadioButtons(
#    options=list(expert_prompts.keys()),
#    description="専門家:",
#)

# ===================
# 20251206改定版
# ===================
expert = st.radio(
    "専門家:",
    list(expert_prompts.keys())
)

# ▼ 質問入力
#query_box = widgets.Text(
#    placeholder="質問を入力してください",
#    description="質問:",
#    layout=widgets.Layout(width="600px")
#)

# ===================
# 20251206改定版
# ===================
question = st.text_input(
    "質問:",
    placeholder="質問を入力してください"
)

# ▼ 送信ボタン
#run_button = widgets.Button(
#    description="送信",
#    button_style="primary"
#)

# ▼ 実行中インジケータ
#status_label = widgets.Label(value="")

# ▼ 出力表示領域
#output = widgets.Output()

# ===================
# 20251206改定版
# （ボタンはイベント処理内で使うため定義不要）
# # ▼ 状態表示領域
# ===================
status_label = st.empty()
output = st.empty()

# ▼ 送信ボタン処理
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
                messages=messages
            )

            response = completion.choices[0].message.content

            status_label.success(f"▼ 選択した専門家: {expert}")
            output.write(response)

        except Exception as e:
            st.error(f"⚠ エラーが発生しました: {e}")

#===================
# 以下は ipywidgets版のまま残す（参考用）
#===================
#def run_query(btn):
#    with output:
#        clear_output()
#        
#        expert = expert_radio.value
#        question = query_box.value
#
#        if not question:
#            print("⚠ 質問を入力してください")
#            return
#        
#        # 🔹 実行中ステータス表示 & ボタン無効化
#        status_label.value = "⏳ 回答生成中です。しばらくお待ちください..."
#        run_button.disabled = True
#        
#        try:
#            messages = [
#                {"role": "system", "content": expert_prompts[expert]},
#                {"role": "user", "content": question}
#            ]
#
#            completion = client.chat.completions.create(
#                model="gpt-4o-mini",
#                temperature=0.5,
#                messages=messages
#            )
#
#            # 🔹 結果表示
#            print(f"▼ 選択した専門家: {expert}\n")
#            print(completion.choices[0].message.content)
#
#        except Exception as e:
#            print(f"⚠ エラーが発生しました: {e}")
#
#        finally:
#            # 🔹 処理完了 → ステータスクリア & ボタン有効化
#            status_label.value = ""
#            run_button.disabled = False
#
#
# ▼ イベント設定
#run_button.on_click(run_query)
#
# ▼ UI表示
#display(expert_radio, query_box, run_button, status_label, output)
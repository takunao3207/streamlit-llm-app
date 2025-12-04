#20251123構築
!pip install langchain==0.3.0 openai==1.47.0 langchain-community==0.3.0 langchain-openai==0.2.2 httpx==0.27.2

import os
from google.colab import userdata
from openai import OpenAI
import ipywidgets as widgets
from IPython.display import display, clear_output

#===================
#20251204追加
from dotenv import load_dotenv
load_dotenv()
#===================

# ▼ API Key設定
os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ▼ 専門家別 system prompt （2人版）
expert_prompts = {
    "健康アドバイザー": "あなたは健康に関する専門家です。エビデンスに基づいた安全なアドバイスをしてください。",
    "ITコンサルタント": "あなたはITコンサルタントです。利用者の業務効率化につながる実用的な助言を提供してください。",
}

#===================
#改定案　20251123
#===================
# ▼ 専門家別 system prompt （2人版）
expert_prompts = {
    "健康アドバイザー": "あなたは健康に関する専門家です。エビデンスに基づいた安全なアドバイスをしてください。",
    "ITコンサルタント": "あなたはITコンサルタントです。業務改善につながる実用的な助言を提供してください。",
}

# ▼ ラジオボタン UI
expert_radio = widgets.RadioButtons(
    options=list(expert_prompts.keys()),
    description="専門家:",
)

# ▼ 質問入力
query_box = widgets.Text(
    placeholder="質問を入力してください",
    description="質問:",
    layout=widgets.Layout(width="600px")
)

# ▼ 送信ボタン
run_button = widgets.Button(
    description="送信",
    button_style="primary"
)

# ▼ 実行中インジケータ
status_label = widgets.Label(value="")

# ▼ 出力表示領域
output = widgets.Output()


def run_query(btn):
    with output:
        clear_output()
        
        expert = expert_radio.value
        question = query_box.value
        
        if not question:
            print("⚠ 質問を入力してください")
            return
        
        # 🔹 実行中ステータス表示 & ボタン無効化
        status_label.value = "⏳ 回答生成中です。しばらくお待ちください..."
        run_button.disabled = True
        
        try:
            messages = [
                {"role": "system", "content": expert_prompts[expert]},
                {"role": "user", "content": question}
            ]

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.5,
                messages=messages
            )

            # 🔹 結果表示
            print(f"▼ 選択した専門家: {expert}\n")
            print(completion.choices[0].message.content)

        except Exception as e:
            print(f"⚠ エラーが発生しました: {e}")

        finally:
            # 🔹 処理完了 → ステータスクリア & ボタン有効化
            status_label.value = ""
            run_button.disabled = False


run_button.on_click(run_query)

# ▼ UI表示
display(expert_radio, query_box, run_button, status_label, output)

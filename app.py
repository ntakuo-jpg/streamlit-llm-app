from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import streamlit as st

# 環境変数の読み込み
load_dotenv()

# OpenAI APIキーの設定
api_key = os.getenv("OPENAI_API_KEY")

# ChatOpenAIインスタンスにAPIキーを渡す
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=api_key)


def get_llm_response(input_text, expert_type):
    """
    入力テキストと専門家の種類に応じてLLMからの回答を取得する関数。

    Args:
        input_text (str): ユーザーが入力したテキスト。
        expert_type (str): 選択された専門家の種類。

    Returns:
        str: LLMからの回答。
    """
    if expert_type == "A: 料理の専門家":
        system_message = "あなたは料理の専門家です。食材に基づいて詳細な料理名を提供してください。"
    elif expert_type == "B: コーヒー豆の専門家":
        system_message = "あなたはコーヒー豆の専門家です。コーヒーの産地や風味について詳しい情報を提供してください。"
    else:
        system_message = "申し訳ありませんが、選択された専門家タイプについては対応しておりません。ご質問内容をもう一度ご確認ください。"

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text),
    ]

    result = llm(messages)
    # result.contentはLLMから返される回答の文字列（str型）です
    return result.content

# StreamlitアプリのUI
st.title("Streamlitを使い、LLM機能を搭載したWebアプリ（LLMアプリ）")

st.write("##### A: 料理の専門家")
st.write("入力フォームに食材を入力し、「実行」ボタンを押すことで料理名が出てきます。")

st.write("##### B: コーヒー豆の専門家")
st.write("コーヒーの産地を入れることで、コーヒーの特徴が出てきます。")

# ラジオボタンで専門家の種類を選択
selected_item = st.radio(
    "動作モードを選択してください。",
    ["A: 料理の専門家", "B: コーヒー豆の専門家"]
)

st.markdown("---")

# 入力フォーム
if selected_item == "A: 料理の専門家":
    input_message = st.text_input(label="食材を入力してください。")
else:
    input_message = st.text_input(label="コーヒーの産地を入力してください。")

# 実行ボタン
if st.button("実行"):
    st.divider()

    if input_message:
        # LLMからの回答を取得
        response = get_llm_response(input_message, selected_item)
        st.write(f"### 専門家からの回答:")
        st.write(response)
    else:
        st.error("テキストを入力してから「実行」ボタンを押してください。")



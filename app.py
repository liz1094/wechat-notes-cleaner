import datetime
import streamlit as st
import requests

st.set_page_config(page_title="微信群聊整理助手", layout="wide")
st.title("📌 微信群聊整理助手")
st.write("请粘贴你在微信中【收藏→转为笔记】的群消息内容，我将帮你整理关键信息！")

user_input = st.text_area("🖊️ 粘贴微信笔记内容：", height=300)

if st.button("🧠 一键整理"):
    with st.spinner("正在分析中..."):
        prompt = f"""以下是微信群消息笔记，请提取重要事项、提醒、和关键信息，生成清晰摘要：\n\n{user_input}"""
        headers = {
            "Authorization": "Bearer sk-你的key",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            result = response.json()

            # 显示原始 JSON（调试用）
            st.json(result)

            if "choices" in result and result["choices"]:
                summary = result["choices"][0]["message"]["content"]
                st.subheader("📄 整理结果")
                st.markdown(summary)

                today = datetime.date.today().isoformat()
                st.download_button(
                    label="📥 下载整理结果",
                    data=summary,
                    file_name=f"wechat_summary_{today}.md",
                    mime="text/markdown"
                )
            else:
                st.write("⚠️ 未获取到有效返回内容。")
        except Exception as e:
            st.write("🚨 请求失败：", str(e))

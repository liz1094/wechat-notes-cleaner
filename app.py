import streamlit as st
import requests
import datetime

# 页面配置
st.set_page_config(page_title="微信群聊整理助手", layout="wide")

st.title("📌 微信群聊整理助手")
st.write("请粘贴你在微信中【收藏-转为笔记】的群消息内容，我将帮你整理关键信息！")

user_input = st.text_area("📋 粘贴微信群笔记内容：", height=300)

if st.button("🧠 一键整理"):
    with st.spinner("正在分析中..."):
        prompt = f"请对下面微信群消息笔记，归纳整理成结构化要点，时间线、活动、分工、重要提醒等，适合直接转发给群成员：\n\n{user_input}"

        headers = {
            "Authorization": "Bearer sk-a2288859e291437598a60d96bb080607",  
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        result = response.json()

        if "choices" in result and result["choices"]:
            summary = result["choices"][0]["message"]["content"]

            st.subheader("📄 整理结果")
            st.markdown(summary)

            today = datetime.date.today().isoformat()

            # 代码块显示内容（方便用户复制）
            st.code(summary, language="markdown")

            # 下载为 Markdown 文件
            st.download_button(
                label="⬇️ 下载为 Markdown",
                data=summary,
                file_name=f"wechat_summary_{today}.md",
                mime="text/markdown"
            )


        else:
            st.warning("⚠️ 没有获取到内容，请检查输入格式或API状态")
            st.json(result) 


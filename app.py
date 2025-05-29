import streamlit as st
import requests

st.set_page_config(page_title="微信群聊整理助手", layout="wide")

st.title("📌 微信群聊整理助手")
st.write("请粘贴你在微信中【收藏→转为笔记】的群消息内容，我将帮你整理关键信息！")

user_input = st.text_area("✏️ 粘贴微信笔记内容：", height=300)

if st.button("🧠 一键整理"):
    with st.spinner("正在分析中..."):
        prompt = f"以下是微信群消息笔记，请提取重要事项、提醒、和关键信息，生成清晰摘要：\n\n{user_input}"
        headers = {
            "Authorization": "Bearer sk-278e27f90ab845619183e24ec00d9ce4",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
        response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
        result = response.json()
       
st.json(result)

if "choices" in result and result["choices"]:
    st.subheader("📄 整理结果")
    import datetime

today_str = datetime.date.today().isoformat()

summary = result["choices"][0]["message"]["content"]

st.subheader("📄 整理结果")
st.markdown(summary)

st.download_button(
    label="📥 下载整理结果",
    data=summary,
    file_name=f"wechat_summary_{today_str}.md",
    mime="text/markdown"
)

else:
    st.write("⚠️ API 返回结构异常，原始数据如下：")
    st.json(result)


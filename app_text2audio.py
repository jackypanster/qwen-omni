import streamlit as st
import uuid
import os
from main_text2audio import text_to_speech

# 输出目录
OUTPUT_DIR = "output"

# Streamlit 页面标题
st.set_page_config(page_title="Qwen2.5-Omni 文本转语音演示", layout="centered")
st.title("Qwen2.5-Omni 文本转语音 (TTS) Web Demo")

# 文本输入
text_input = st.text_area("请输入要合成的文本：", height=120, max_chars=200)

# 发音人选择
speaker = st.selectbox("请选择发音人：", ["Chelsie", "Ethan"], index=0)

# 生成按钮
if st.button("生成语音"):
    if not text_input.strip():
        st.warning("请输入文本后再生成语音！")
    else:
        # 生成唯一音频文件名
        audio_filename = f"tts_{uuid.uuid4().hex}.wav"
        audio_path = os.path.join(OUTPUT_DIR, audio_filename)
        
        # 生成过程提示
        with st.spinner("正在生成语音，请稍候..."):
            try:
                text_to_speech(text_input, output_audio_path=audio_path, speaker=speaker)
                st.success("语音生成成功！")
                # 播放音频
                audio_bytes = open(audio_path, "rb").read()
                st.audio(audio_bytes, format="audio/wav")
                # 可选：显示生成文本
                st.write("**生成文本：**", text_input)
            except Exception as e:
                st.error(f"语音生成失败: {e}")

# 版权信息
st.markdown("<hr/><center>Qwen2.5-Omni-7B 文本转语音演示 | Powered by Streamlit</center>", unsafe_allow_html=True)

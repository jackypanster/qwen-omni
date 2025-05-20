# Streamlit 文本转语音 Web 页面实现方案

## 设计目标
为 Qwen2.5-Omni-7B 文本转语音功能提供一个简洁易用的 Web 页面，方便用户输入文字并在线收听生成的语音。

## 实现步骤
1. **新建 Streamlit 页面文件**
   - 建议命名为 `app_text2audio.py` 或 `web_text2audio.py`。

2. **页面结构设计**
   - 文本输入框（st.text_area）
   - 发音人选择（st.selectbox）
   - 生成按钮（st.button）
   - 生成进度提示（st.spinner）
   - 生成文本展示（st.write，可选）
   - 音频播放控件（st.audio）

3. **后端集成**
   - 通过 import main_text2audio.py 的 text_to_speech 函数实现音频生成。
   - 生成音频文件时，使用 uuid 或时间戳命名，防止多用户/多次请求冲突。
   - 生成后返回音频文件路径，供 st.audio 播放。

4. **模型加载优化**
   - 在 Streamlit 启动时全局加载模型和 processor，避免每次请求重复加载（可用 st.cache_resource 或全局变量）。

5. **异常处理与用户体验**
   - 生成失败时给出友好提示。
   - 生成过程中显示"正在生成"提示。

## 重要说明
**严禁修改 main_text2audio.py 的内容。**
- 仅通过 import 方式调用 text_to_speech 函数。
- 保证 main_text2audio.py 的独立性和可维护性。

---
本设计文档为前端实现和后续维护提供参考。

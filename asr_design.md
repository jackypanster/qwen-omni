# Qwen2.5-Omni-7B 语音转文本（ASR）设计文档

## 目标
基于 Qwen2.5-Omni-7B 实现语音转文本（ASR），用于理解用户语音指令。

## 实现方式
- 复用 Qwen2.5-Omni-7B 多模态能力，构造多模态 conversation，user content 为 audio 类型。
- 使用 Qwen2_5OmniForConditionalGeneration 和 Qwen2_5OmniProcessor 进行推理。
- 参考官方文档的"Conversation with audio only"用法。

## 接口设计
### audio_to_text(audio_path: str) -> str
- 输入：音频文件路径（如 wav）
- 输出：转录文本字符串
- 主要流程：
  1. 构造 conversation，user content 为 audio
  2. 用 processor 处理输入，生成模型输入张量
  3. 调用 model.generate，返回文本 token
  4. processor.batch_decode 得到最终文本

### audio_to_text_pure_asr(audio_path: str) -> str
- 输入：音频文件路径（如 wav）
- 输出：最大程度还原原始语音内容的转录文本
- 特点：
  - 尝试调用 disable_talker()，禁用智能化
  - max_new_tokens=0，强制只输出ASR结果
  - prompt 明确要求"只做转录，不润色"

## 输入输出格式
- 输入：本地音频文件路径（支持 wav 等格式）
- 输出：转录后的文本字符串

## 注意事项
- 系统 prompt 必须为官方推荐内容，保证模型正确理解音频输入
- 仅需文本输出，`return_audio=False`
- 可根据实际需求调整 max_new_tokens 等参数

## 示例
```python
asr_text = audio_to_text("/path/to/audio.wav")
print(asr_text)  # 输出：购买1000股广发股票
asr_text_pure = audio_to_text_pure_asr("/path/to/audio.wav")
print(asr_text_pure)  # 输出：原始语音内容，无润色
```

## FastAPI RESTful API 设计

### 接口1：POST /asr
- 功能：接收用户上传的音频文件，调用 audio_to_text 进行转录，返回文本结果。
- 适用场景：允许模型适度理解和补全，适合通用语音理解。

#### 请求示例
```bash
curl -X POST "http://localhost:8000/asr" -F "file=@/home/user/Downloads/test_audio.wav"
```

#### 成功响应示例
```json
{
  "success": true,
  "text": "购买1000股广发股票"
}
```

### 接口2：POST /asr_pure
- 功能：接收用户上传的音频文件，调用 audio_to_text_pure_asr，只做ASR、禁用智能化，最大程度还原原始语音内容。
- 适用场景：对原文还原度要求极高的金融、法律等场景。

#### 请求示例
```bash
curl -X POST "http://localhost:8000/asr_pure" -F "file=@/home/user/Downloads/test_audio.wav"
```

#### 成功响应示例
```json
{
  "success": true,
  "text": "购买一千股广发股票"  // 仅为示例，实际输出为原始语音内容
}
```

#### 失败响应示例
```json
{
  "success": false,
  "error": "音频文件无效或转录失败"
}
```

### 常见问题与解决方法
- **curl: (26) Failed to open/read local data from file/application**
  - 解决：curl 的 -F 路径不能用 ~，请用绝对路径或当前目录下的相对路径。
- **Form data requires "python-multipart" to be installed**
  - 解决：在 uv/conda/pip 环境中安装 python-multipart。
- **接口返回 400，提示文件类型不支持**
  - 解决：请上传 wav、mp3、m4a、flac 格式的音频文件。

### 设计要点
- 接口校验文件类型和大小，防止异常输入。
- 支持多种常见音频格式。
- /asr_pure 返回的 text 字段为最大程度还原的转录文本。

## 后续扩展
- 可结合指令解析模块，实现更复杂的语音指令理解。
- 可增加异步队列、任务状态查询等功能，提升并发能力。 
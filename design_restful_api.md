# FastAPI 文本转语音 RESTful 接口设计方案

## 方案背景
由于 Python 依赖环境复杂，直接用 Web UI（如 Streamlit）集成大模型推理容易遇到兼容性问题。为降低环境耦合度，推荐采用 FastAPI 提供 RESTful API 服务，底层只需保证 main_text2audio.py 能正常运行。

## 方案优点
- **环境隔离**：只要 main_text2audio.py 能在本地命令行跑通，API 层无需关心底层依赖的复杂性。
- **接口简单**：只需 POST 文本，返回音频文件名或下载链接，前端/第三方系统易于集成。
- **易于维护和扩展**：后续可加队列、鉴权、日志、限流等功能，支持多用户并发。
- **与前端解耦**：前端只需请求 API，下载音频即可。

## 推荐实现思路
1. **新建 fastapi_app.py**
   - 提供 `/tts` POST 接口，接收文本和可选参数（如 speaker）。
   - 调用 main_text2audio.py 的 text_to_speech，生成音频文件。
   - 返回 JSON：`{"success": true, "audio_file": "output/xxx.wav"}`
2. **提供静态文件服务**
   - 用 FastAPI 的 StaticFiles 挂载 output 目录，用户可直接下载音频。
3. **main_text2audio.py 保持不变**
   - fastapi_app.py 只 import 并调用其函数。
4. **部署**
   - 用 `uvicorn fastapi_app:app --host 0.0.0.0 --port 8000` 启动服务。

## 典型接口示例
- **POST /tts**
  - 请求体：`{"text": "你好，世界", "speaker": "Chelsie"}`
  - 返回：`{"success": true, "audio_file": "output/tts_xxx.wav"}`
- **GET /output/tts_xxx.wav**
  - 直接下载音频

## HTTP POST /tts 测试用例

### 1. curl 命令示例
```bash
curl -X POST "http://localhost:8000/tts" \
     -H "Content-Type: application/json" \
     -d '{"text": "你好，世界！这是测试。", "speaker": "Chelsie"}'
```

### 2. 请求体示例
```json
{
  "text": "你好，世界！这是测试。",
  "speaker": "Chelsie"
}
```

### 3. 成功响应示例
```json
{
  "success": true,
  "audio_file": "/output/tts_1234567890abcdef.wav"
}
```

### 4. 失败响应示例（如文本为空）
```json
{
  "detail": "文本不能为空"
}
```

---

## 总结
- 该方案适合当前环境和需求，能极大降低环境兼容性带来的麻烦。
- 推荐用 FastAPI 实现 RESTful 服务，主流程只需调用 main_text2audio.py。
- 后续如需前端页面，可直接请求 API，或用 curl/postman 测试。

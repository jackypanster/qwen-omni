# Qwen2.5-Omni 文本转语音（TTS）与语音转文本（ASR）Web Demo

本项目基于 Qwen2.5-Omni-7B，提供文本转语音（TTS）和语音转文本（ASR）两大功能，支持 Web 演示界面和 RESTful API。**推荐使用 [conda](https://docs.conda.io/) 管理 Python 环境**，兼容性更好。uv 方案可作为可选补充。

---

## 最新进展与主要功能

- ✅ **文本转语音（TTS）**：输入文本，生成语音文件，支持多发音人。
- ✅ **语音转文本（ASR）**：输入音频文件，输出转录文本。
    - 标准ASR：允许模型适度理解和补全，适合通用语音理解。
    - 纯ASR（/asr_pure）：禁用智能化，最大程度还原原始语音内容，适合金融、法律等场景。
- ✅ **RESTful API**：已实现 /tts、/asr、/asr_pure 等接口，支持 HTTP 文件上传与文本转写。
- ✅ **文档与测试用例**：同步完善了 asr_design.md、design_restful_api.md、python_env_management.md 等文档，便于开发、测试和维护。

---

## 环境准备（推荐 conda 方案）

### 1. 安装 Anaconda 或 Miniconda

请参考 [conda 官方文档](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) 安装。

### 2. 创建并激活 conda 环境

```bash
conda create -n qwen-tts python=3.10
conda activate qwen-tts
```

### 3. 安装依赖

优先用 conda 安装大包和底层依赖，其余用 pip：

```bash
# 安装 PyTorch（如需 GPU 版本请参考 https://pytorch.org/ 官网说明）
conda install pytorch=2.5.1 pytorch-cuda=12.1 -c pytorch -c nvidia
# 让 conda 自动匹配兼容的 torchvision、torchaudio 版本
conda install torchvision torchaudio -c pytorch

# 安装 streamlit、soundfile（底层依赖更稳）
conda install streamlit python-soundfile -c conda-forge

# 安装 Qwen2.5-Omni 专用 transformers（必须用 pip+git）
pip install git+https://github.com/huggingface/transformers@v4.51.3-Qwen2.5-Omni-preview

# 安装 qwen-omni-utils（只能用 pip）
pip install qwen-omni-utils
```

如有 requirements.txt，可用：
```bash
pip install -r requirements.txt
```

---

## 启动与运行

### 1. 启动 Web 页面（Streamlit）
```bash
streamlit run app_text2audio.py
```

### 2. 启动 RESTful API 服务（FastAPI）
```bash
uv run uvicorn fastapi_app:app --host 0.0.0.0 --port 8000
```

---

## RESTful API 典型接口

- **POST /tts**：文本转语音，返回音频文件下载链接
- **POST /asr**：语音转文本（标准ASR）
- **POST /asr_pure**：语音转文本（纯ASR，禁用智能化）

详见 asr_design.md、design_restful_api.md

---

## 常见问题

- 如遇依赖未找到，确认已激活 conda 环境（`which python` 路径应在 conda envs 目录下）。
- 若模型文件较大，建议提前下载好并配置好 `main_text2audio.py` 中的模型路径。
- 如需安装新依赖，优先用 conda 安装，conda 没有的再用 pip。
- transformers 必须用 Qwen2.5-Omni 官方定制版（pip+git 安装）。
- curl 上传文件时请用绝对路径，不要用 ~。
- FastAPI 文件上传需安装 python-multipart。

---

## 目录结构示例

```
├── app_text2audio.py         # Streamlit 前端页面
├── main_text2audio.py        # 文本转语音/语音转文本核心逻辑
├── fastapi_app.py            # RESTful API 服务
├── output/                   # 生成的音频文件目录
├── asr_design.md             # ASR 设计与接口文档
├── design_restful_api.md     # RESTful API 设计文档
├── docs/python_env_management.md # 环境管理对比与经验
├── README.md                 # 本说明文档
└── ...
```

---

## 可选：uv 环境管理方案

如需体验 uv，可参考以下流程：

1. 安装 uv
   ```bash
   pip install uv
   ```
2. 初始化 uv 虚拟环境
   ```bash
   uv venv init
   uv venv shell
   source shell/bin/activate
   ```
3. 安装依赖
   ```bash
   uv add streamlit soundfile torch transformers qwen-omni-utils
   ```
4. 启动 Web 页面
   ```bash
   streamlit run app_text2audio.py
   ```

---

## 参考
- [Qwen2.5-Omni-7B 官方文档](https://huggingface.co/Qwen/Qwen2.5-Omni-7B)
- [conda 官方文档](https://docs.conda.io/)
- [uv 官方文档](https://github.com/astral-sh/uv)
- asr_design.md、design_restful_api.md、docs/python_env_management.md

---

如有问题欢迎提 issue 或联系维护者。

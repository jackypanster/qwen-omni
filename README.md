# Qwen2.5-Omni 文本转语音（TTS）Web Demo

本项目基于 Qwen2.5-Omni-7B，提供文本转语音的 Web 演示界面。**推荐使用 [conda](https://docs.conda.io/) 管理 Python 环境**，兼容性更好。uv 方案可作为可选补充。

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

```bash
streamlit run app_text2audio.py
```

---

## 常见问题

- 如遇依赖未找到，确认已激活 conda 环境（`which python` 路径应在 conda envs 目录下）。
- 若模型文件较大，建议提前下载好并配置好 `main_text2audio.py` 中的模型路径。
- 如需安装新依赖，优先用 conda 安装，conda 没有的再用 pip。
- transformers 必须用 Qwen2.5-Omni 官方定制版（pip+git 安装）。

---

## 目录结构示例

```
├── app_text2audio.py         # Streamlit 前端页面
├── main_text2audio.py        # 文本转语音核心逻辑
├── output/                   # 生成的音频文件目录
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

---

如有问题欢迎提 issue 或联系维护者。

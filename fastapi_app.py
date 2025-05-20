from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
import os
from main_text2audio import text_to_speech, audio_to_text
import shutil

app = FastAPI(title="Qwen2.5-Omni 文本转语音 RESTful API")

# 挂载 output 目录，供音频文件下载
app.mount("/output", StaticFiles(directory="output"), name="output")

class TTSRequest(BaseModel):
    text: str
    speaker: str = "Chelsie"  # 默认发音人

@app.post("/tts")
async def tts_api(req: TTSRequest):
    text = req.text.strip()
    speaker = req.speaker
    if not text:
        raise HTTPException(status_code=400, detail="文本不能为空")
    # 生成唯一音频文件名
    audio_filename = f"tts_{uuid.uuid4().hex}.wav"
    audio_path = os.path.join("output", audio_filename)
    try:
        text_to_speech(text, output_audio_path=audio_path, speaker=speaker)
        return JSONResponse({
            "success": True,
            "audio_file": f"/output/{audio_filename}"
        })
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": str(e)
        }, status_code=500)

@app.post("/asr")
async def asr_api(file: UploadFile = File(...)):
    # 校验文件类型
    if not file.filename.lower().endswith((".wav", ".mp3", ".m4a", ".flac")):
        return JSONResponse({"success": False, "error": "仅支持wav/mp3/m4a/flac音频文件"}, status_code=400)
    # 保存上传的音频到临时文件
    tmp_path = f"output/asr_{uuid.uuid4().hex}_{file.filename}"
    try:
        with open(tmp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # 调用ASR
        text = audio_to_text(tmp_path)
        return JSONResponse({"success": True, "text": text})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

# 健康检查接口
@app.get("/ping")
def ping():
    return {"msg": "pong"}

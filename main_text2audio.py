import os
import soundfile as sf
import torch
from transformers import Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor
from qwen_omni_utils import process_mm_info
from transformers import AutoConfig

def text_to_speech(text_input, output_audio_path="output/output.wav", speaker="Chelsie"):
    model_path = "/home/llm/model/qwen/Omni/"
    
    # 修复 ROPE 参数兼容性
    config = AutoConfig.from_pretrained(model_path, local_files_only=True)
    if hasattr(config, 'rope_scaling') and 'mrope_section' in config.rope_scaling:
        config.rope_scaling.pop('mrope_section')
    
    # 加载模型（不使用 FlashAttention2）
    model = Qwen2_5OmniForConditionalGeneration.from_pretrained(
        model_path, config=config, torch_dtype="auto", device_map="auto", local_files_only=True
    )
    processor = Qwen2_5OmniProcessor.from_pretrained(model_path, local_files_only=True)
    
    # 系统提示
    system_prompt = [
        {"role": "system", "content": [
            {"type": "text", "text": "You are Qwen...generating text and speech."}  # 省略重复内容
        ]}
    ]
    
    conversation = system_prompt + [{"role": "user", "content": [{"type": "text", "text": text_input}]}]
    
    # 处理输入
    text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    audios, images, videos = process_mm_info(conversation, use_audio_in_video=False)
    
    inputs = processor(
        text=text, audio=audios, images=images, videos=videos, 
        return_tensors="pt", padding=True, use_audio_in_video=False
    ).to(model.device, model.dtype)
    
    # 生成参数优化：启用采样模式
    with torch.no_grad():
        text_ids, audio = model.generate(
            **inputs,
            speaker=speaker,
            do_sample=True,  # 新增：启用采样模式
            temperature=0.8,
            top_p=0.95,
            max_new_tokens=1024
        )
    
    # 解析结果
    generated_text = processor.batch_decode(text_ids, skip_special_tokens=True)[0]
    print(f"生成文本: {generated_text}")
    
    # 修复路径问题：确保目录存在
    output_dir = os.path.dirname(output_audio_path)
    if output_dir and not os.path.exists(output_dir):  # 处理空目录（如当前目录）
        os.makedirs(output_dir, exist_ok=True)
    sf.write(output_audio_path, audio.reshape(-1).cpu().numpy(), samplerate=24000)
    print(f"音频已保存至: {output_audio_path}")

def audio_to_text(audio_path: str) -> str:
    """
    语音转文本（ASR），输入音频文件路径，返回转录文本。
    """
    model_path = "/home/llm/model/qwen/Omni/"
    # 加载模型配置
    config = AutoConfig.from_pretrained(model_path, local_files_only=True)
    if hasattr(config, 'rope_scaling') and 'mrope_section' in config.rope_scaling:
        config.rope_scaling.pop('mrope_section')
    # 加载模型和处理器
    model = Qwen2_5OmniForConditionalGeneration.from_pretrained(
        model_path, config=config, torch_dtype="auto", device_map="auto", local_files_only=True
    )
    processor = Qwen2_5OmniProcessor.from_pretrained(model_path, local_files_only=True)
    # 构造多模态输入（audio only）
    system_prompt = [
        {"role": "system", "content": [
            {"type": "text", "text": "你是Qwen，一个由阿里巴巴集团Qwen团队开发的虚拟人。请你将用户上传的音频内容逐字转录为文本，不要润色、改写或补全，只需尽量还原原始语音内容。"}
        ]}
    ]
    conversation = system_prompt + [
        {"role": "user", "content": [
            {"type": "audio", "audio": audio_path}
        ]}
    ]
    text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    audios, images, videos = process_mm_info(conversation, use_audio_in_video=False)
    inputs = processor(
        text=text, audio=audios, images=images, videos=videos,
        return_tensors="pt", padding=True, use_audio_in_video=False
    ).to(model.device, model.dtype)
    with torch.no_grad():
        text_ids = model.generate(
            **inputs,
            do_sample=False,
            max_new_tokens=1024,
            return_audio=False
        )
    asr_text = processor.batch_decode(text_ids, skip_special_tokens=True)[0]
    return asr_text

if __name__ == "__main__":
    # 指定带目录的输出路径（避免根目录问题）
    input_text = "你好，这是修复后的音频生成测试，路径问题已解决。"
    text_to_speech(input_text, output_audio_path="output/test_audio.wav", speaker="Chelsie")

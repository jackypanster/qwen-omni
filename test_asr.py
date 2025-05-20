from main_text2audio import audio_to_text

if __name__ == "__main__":
    wav_path = "output/test_audio.wav"
    result = audio_to_text(wav_path)
    print(f"{wav_path} 的转录结果：{result}")

    wav_path2 = "output/tts_f67ce04c10b64a5f971635366cb85d8f.wav"
    result2 = audio_to_text(wav_path2)
    print(f"{wav_path2} 的转录结果：{result2}")
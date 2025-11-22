import logging
import os
import base64
import signal
import sys
import time
import dashscope
from dashscope.audio.qwen_omni import *
from dashscope.audio.qwen_omni.omni_realtime import TranscriptionParams
from dotenv import load_dotenv

# 載入 .env 文件
load_dotenv()


def setup_logging():
    """配置日志输出"""
    logger = logging.getLogger('dashscope')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def init_api_key():
    """初始化 API Key"""
    # 新加坡和北京地域的API Key不同。获取API Key：https://www.alibabacloud.com/help/zh/model-studio/get-api-key
    # 若没有配置环境变量，请用百炼API Key将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY', 'YOUR_API_KEY')
    if dashscope.api_key == 'sk-e295e8477c31449890bb371bf8d6f6b4':
        print('[Warning] Using placeholder API key, set DASHSCOPE_API_KEY environment variable.')


class MyCallback(OmniRealtimeCallback):
    """实时识别回调处理"""
    def __init__(self, conversation):
        self.conversation = conversation
        self.handlers = {
            'session.created': self._handle_session_created,
            'conversation.item.input_audio_transcription.completed': self._handle_final_text,
            'conversation.item.input_audio_transcription.text': self._handle_stash_text,
            'input_audio_buffer.speech_started': lambda r: print('======Speech Start======'),
            'input_audio_buffer.speech_stopped': lambda r: print('======Speech Stop======'),
            'response.done': self._handle_response_done
        }

    def on_open(self):
        print('Connection opened')

    def on_close(self, code, msg):
        print(f'Connection closed, code: {code}, msg: {msg}')

    def on_event(self, response):
        try:
            handler = self.handlers.get(response['type'])
            if handler:
                handler(response)
        except Exception as e:
            print(f'[Error] {e}')

    def _handle_session_created(self, response):
        print(f"Start session: {response['session']['id']}")

    def _handle_final_text(self, response):
        print(f"Final recognized text: {response['transcript']}")

    def _handle_stash_text(self, response):
        print(f"Got stash result: {response['stash']}")

    def _handle_response_done(self, response):
        print('======RESPONSE DONE======')
        print(f"[Metric] response: {self.conversation.get_last_response_id()}")


def read_audio_chunks(file_path, chunk_size=3200):
    """按块读取音频文件"""
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            yield chunk


def send_audio(conversation, file_path, delay=0.1):
    """发送音频数据"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file {file_path} does not exist.")

    print("Processing audio file... Press 'Ctrl+C' to stop.")
    for chunk in read_audio_chunks(file_path):
        audio_b64 = base64.b64encode(chunk).decode('ascii')
        conversation.append_audio(audio_b64)
        time.sleep(delay)
    # enable_turn_detection为False时，应将下行代码注释取消
    # conversation.commit()
    # print("Audio commit sent.")

def send_silence_data(conversation, cycles=30, bytes_per_cycle=1024):
    # 创建1024字节的静音数据（全零）
    silence_data = bytes(bytes_per_cycle)

    for i in range(cycles):
        # 将字节数据编码为base64
        audio_b64 = base64.b64encode(silence_data).decode('ascii')
        # 发送静音数据
        conversation.append_audio(audio_b64)
        time.sleep(0.01)  # 10毫秒延迟
    print(f"已发送 {cycles} 次静音数据，每次 {bytes_per_cycle} 字节")

def main():
    setup_logging()
    init_api_key()

    audio_file_path = "./your_audio_file.pcm"
    conversation = OmniRealtimeConversation(
        model='qwen3-asr-flash-realtime',
        
        url='wss://dashscope-intl.aliyuncs.com/api-ws/v1/realtime',
        callback=MyCallback(conversation=None)  # 暂时传None，稍后注入
    )

    # 注入自身到回调
    conversation.callback.conversation = conversation

    def handle_exit(sig, frame):
        print('Ctrl+C pressed, exiting...')
        conversation.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_exit)

    conversation.connect()

    transcription_params = TranscriptionParams(
        language='zh',
        sample_rate=16000,
        input_audio_format="pcm"
        # 输入音频的语料，用于辅助识别
        # corpus_text=""
    )

    conversation.update_session(
        output_modalities=[MultiModality.TEXT],
        enable_input_audio_transcription=True,
        transcription_params=transcription_params
    )

    try:
        send_audio(conversation, audio_file_path)
        # 追加发送静音音频，防止音频文件尾部没有静音导致无法判停
        send_silence_data(conversation)
        time.sleep(3)  # 等待响应
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        conversation.close()
        print("Audio processing completed.")


if __name__ == '__main__':
    main()
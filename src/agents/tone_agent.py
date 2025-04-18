from .base_agent import BaseAgent
import openai

class ToneAdjusterAgent(BaseAgent):
    def __init__(self):
        super().__init__("ToneAdjusterAgent")

    def process(self, text: str, tone: str = "正式") -> str:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一位语言风格专家，擅长调整语气。"},
                    {"role": "user", "content": f"请将以下文本调整为 {tone} 语气：\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[ToneAdjusterAgent] 语气调整失败：{str(e)}"

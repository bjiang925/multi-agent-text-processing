import openai

class ToneAdjusterAgent:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)  # ✅ 用 OpenAI 官方新客户端

    def run(self, text: str, tone: str = "formal") -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in adjusting writing tone."},
                    {"role": "user", "content": f"Please adjust the tone of the following text to {tone}:\n\n{text}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[ToneAdjusterAgent] Failed to adjust tone: {str(e)}"

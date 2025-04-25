import openai

class TranslationAgent:
    def __init__(self, api_key, target_language="Chinese"):
        self.client = openai.OpenAI(api_key=api_key)
        self.target_language = target_language

    def run(self, text: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a helpful translator. Translate everything to {self.target_language}."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[TranslationAgent] Failed: {str(e)}"

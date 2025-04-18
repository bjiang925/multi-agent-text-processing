import openai

class TranslationAgent:
    def __init__(self, target_language, api_key):
        self.target_language = target_language
        openai.api_key = api_key

    def process(self, text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are a helpful translator to {self.target_language}."},
                    {"role": "user", "content": f"Please translate this text: {text}"}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

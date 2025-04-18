import openai

class StyleEnhancerAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        openai.api_key = "sk-请在这里填入你自己的key"
        self.model = model

    def enhance_style(self, text: str) -> str:
        prompt = f"""
        Please improve the style of the following text. Enhance vocabulary, improve sentence structure, and make the tone more polished — but do not change the meaning.

        Original:
        {text}

        Enhanced version:
        """
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional writing assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {str(e)}"

import openai

class StyleEnhancerAgent:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def run(self, text: str) -> str:
        prompt = (
            "Please improve the style of the following text. "
            "Enhance vocabulary, improve sentence structure, and make the tone more polished — "
            "but do not change the meaning.\n\n"
            f"Original:\n{text}\n\nEnhanced version:"
        )
        try:
            response = self.client.chat.completions.create(
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
            return f"[StyleEnhancerAgent] Failed: {str(e)}"

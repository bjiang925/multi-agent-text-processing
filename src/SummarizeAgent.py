import openai

class SummarizeAgent:
    """SummarizeAgent: Generate a summary for the input text using OpenAI's chat API."""

    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def run(self, text: str) -> str:
        try:
            prompt = f"Please summarize the following text in 2-3 sentences:\n\n{text}"
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[SummarizeAgent] Failed: {str(e)}"

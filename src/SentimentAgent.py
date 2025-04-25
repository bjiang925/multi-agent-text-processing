import openai
import json

class SentimentAgent:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def run(self, text):
        prompt = f"""
        Please analyze the sentiment of the following text. 
        Respond in JSON format with:
        - sentiment: "positive", "neutral", or "negative"
        - score: a float between -1 and 1
        - explanation: a brief explanation

        Text: {text}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful sentiment analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            reply = response.choices[0].message.content.strip()

            result = json.loads(reply)
            return (
                f"Sentiment: {result.get('sentiment')}\n"
                f"Score: {result.get('score')}\n"
                f"Explanation: {result.get('explanation')}"
            )
        except Exception as e:
            return f"[SentimentAgent] Failed: {str(e)}"

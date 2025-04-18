import openai
import json

class SentimentAgent:
    def __init__(self, model="gpt-3.5-turbo"):
        openai.api_key = "sk-请在这里填入你自己的key"
        self.model = model

    def process(self, text):
        prompt = f"""
        Please analyze the sentiment of the following text. 
        Respond in JSON format with:
        - sentiment: "positive", "neutral", or "negative"
        - score: a float between -1 and 1
        - explanation: a brief explanation
        
        Text: {text}
        """

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        reply = response['choices'][0]['message']['content']
        try:
            result = json.loads(reply)
            return result
        except json.JSONDecodeError:
            return {"error": "Invalid JSON returned", "raw": reply}

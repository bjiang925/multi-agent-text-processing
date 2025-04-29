import openai
import json
import re

class SentimentAgent:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def run(self, text: str) -> str:
        prompt = (
            "Analyze the sentiment of the following text. "
            "Return only valid JSON with three keys: `sentiment` "
            "(positive, neutral, or negative), `score` (float between -1 and 1), "
            "and `explanation` (brief string). No markdown formatting.\n\n"
            f"{text}"
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful sentiment analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            reply = response.choices[0].message.content.strip()

            reply = re.sub(r"^```(?:json)?\\s*|\\s*```$", "", reply.strip(), flags=re.MULTILINE)

            try:
                result = json.loads(reply)
                return (
                    f"Sentiment: {result['sentiment']}\n"
                    f"Score: {result['score']}\n"
                    f"Explanation: {result['explanation']}"
                )
            except Exception as parse_err:
                return f"[SentimentAgent] JSON parsing failed: {str(parse_err)}\n\nRaw reply:\n{reply}"

        except Exception as e:
            return f"[SentimentAgent] LLM call failed: {str(e)}"

import openai
import json

class ReadabilityScorerAgent:
    """ ReadabilityScorerAgent: Test readability level of the input text using metrics """
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model  = model

    def run(self, text: str) -> str:
        prompt = (
            "Please compute the Flesch Reading Ease and Flesch–Kincaid Grade Level "
            "for the following text, and return JSON with keys "
            "`flesch_reading_ease` and `flesch_kincaid_grade`:\n\n"
            f"{text}"
        )

        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a readability analysis assistant."},
                    {"role": "user",   "content": prompt}
                ],
                temperature=0
            )
            # parse the assistant’s JSON response
            result = json.loads(resp.choices[0].message.content)
            return (
                f"Flesch Reading Ease: {result['flesch_reading_ease']}\n"
                f"Flesch–Kincaid Grade: {result['flesch_kincaid_grade']}"
            )

        except Exception as e:
            # gracefully handle any API or parsing errors
            return f"[ReadabilityScorerAgent] LLM call failed: {str(e)}"
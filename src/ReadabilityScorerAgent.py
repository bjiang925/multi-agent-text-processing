import openai
import json
import re

class ReadabilityScorerAgent:
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model  = model

    def run(self, text: str) -> str:
        if len(text.split()) > 1200:
            return "[ReadabilityScorerAgent] Input too long. Please shorten the text."

        prompt = (
            "Compute the Flesch Reading Ease and Flesch–Kincaid Grade Level "
            "for the following text. Return only valid JSON with two keys: "
            "`flesch_reading_ease` and `flesch_kincaid_grade`. Do not use Markdown.\n\n"
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

            reply = resp.choices[0].message.content.strip()

            # ✅ 正确的正则清理 Markdown 格式
            reply = re.sub(r"^```(?:json)?\s*|```$", "", reply.strip(), flags=re.MULTILINE)

            try:
                result = json.loads(reply)
                return (
                    f"Flesch Reading Ease: {result['flesch_reading_ease']}\n"
                    f"Flesch–Kincaid Grade: {result['flesch_kincaid_grade']}"
                )
            except Exception as parse_err:
                return f"[ReadabilityScorerAgent] JSON parsing failed: {str(parse_err)}\n\nRaw reply:\n{reply}"

        except Exception as e:
            return f"[ReadabilityScorerAgent] LLM call failed: {str(e)}"

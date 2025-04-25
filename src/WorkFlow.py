from src.SummarizeAgent import SummarizeAgent
from src.ReadabilityScorerAgent import ReadabilityScorerAgent
from src.SentimentAgent import SentimentAgent
from src.StyleEnhancerAgent import StyleEnhancerAgent
from src.ToneAgent import ToneAdjusterAgent
from src.TranslationAgent import TranslationAgent

class Workflow:
    def run_all_agents(self, text: str, tone: str = "formal", target_language: str = "Chinese", api_key: str = None):
        results = {}

        try:
            tone_agent = ToneAdjusterAgent(api_key)
            results["tone"] = tone_agent.run(text, tone=tone)
        except Exception as e:
            results["tone"] = f"ToneAdjusterAgent failed: {str(e)}"

        try:
            sentiment_agent = SentimentAgent(api_key)
            results["sentiment"] = sentiment_agent.run(text)
        except Exception as e:
            results["sentiment"] = f"SentimentAgent failed: {str(e)}"

        try:
            style_agent = StyleEnhancerAgent(api_key)
            results["style"] = style_agent.run(text)
        except Exception as e:
            results["style"] = f"StyleEnhancerAgent failed: {str(e)}"

        try:
            translation_agent = TranslationAgent(api_key, target_language)
            results["translation"] = translation_agent.run(text)
        except Exception as e:
            results["translation"] = f"TranslationAgent failed: {str(e)}"

        try:
            readability_agent = ReadabilityScorerAgent(api_key)
            results["readability"] = readability_agent.run(text)
        except Exception as e:
            results["readability"] = f"ReadabilityScorerAgent failed: {str(e)}"

        try:
            summarize_agent = SummarizeAgent(api_key)
            results["summary"] = summarize_agent.run(text)
        except Exception as e:
            results["summary"] = f"SummarizeAgent failed: {str(e)}"

        return results

    def run_agent(self, agent: str, text: str, api_key: str):
        if agent == "SummarizeAgent":
            return SummarizeAgent(api_key).run(text)
        elif agent == "ReadabilityScorerAgent":
            return ReadabilityScorerAgent(api_key).run(text)
        elif agent == "SentimentAgent":
            return SentimentAgent(api_key).run(text)
        elif agent == "StyleEnhancerAgent":
            return StyleEnhancerAgent(api_key).run(text)
        elif agent == "ToneAdjusterAgent":
            return ToneAdjusterAgent(api_key).run(text, tone="formal")
        elif agent == "TranslationAgent":
            return TranslationAgent(api_key, target_language="Chinese").run(text)
        else:
            return "Unknown agent name."

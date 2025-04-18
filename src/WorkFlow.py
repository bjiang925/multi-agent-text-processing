from src.agents.tone_agent import ToneAdjusterAgent
from src.SentimentAgent import SentimentAgent
from src.StyleEnhancerAgent import StyleEnhancerAgent
from src.TranslationAgent import TranslationAgent
from src.ReadabilityScorerAgent import ReadabilityScorerAgent
from src.SummarizeAgent import SummarizerAgent

class workflow:
    def run_all_agents(text: str, tone: str = "正式", target_language: str = "Chinese", api_key: str = None):
        results = {}

        # ToneAdjusterAgent - now includes tone
        try:
            tone_agent = ToneAdjusterAgent()
            results["tone_adjusted"] = tone_agent.process(text, tone=tone)
        except Exception as e:
            results["tone_adjusted"] = f"ToneAdjusterAgent failed: {str(e)}"

        # SentimentAgent
        try:
            sentiment_agent = SentimentAgent()
            results["sentiment"] = sentiment_agent.process(text)
        except Exception as e:
            results["sentiment"] = f"SentimentAgent failed: {str(e)}"

        # StyleEnhancerAgent
        try:
            style_agent = StyleEnhancerAgent()
            results["style_enhanced"] = style_agent.enhance_style(text)
        except Exception as e:
            results["style_enhanced"] = f"StyleEnhancerAgent failed: {str(e)}"

        # TranslationAgent
        try:
            translation_agent = TranslationAgent(target_language=target_language, api_key=api_key)
            results["translated"] = translation_agent.process(text)
        except Exception as e:
            results["translated"] = f"TranslationAgent failed: {str(e)}"

        # ReadabilityScorerAgent
        try:
            readability_agent = ReadabilityScorerAgent()
            readability_scores = readability_agent.assess_readability(text)
            results["readability"] = readability_scores
        except Exception as e:
            results["readability"] = f"ReadabilityScorerAgent failed: {str(e)}"
            
        # SummarizerAgent
        try:
            summarizer_agent = SummarizerAgent()
            results["summarizer"] = summarizer_agent.process(text)
        except Exception as e:
            results["summarizer"] = f"SummarizerAgent failed: {str(e)}"

        return results

    def run_agent(agent: str, text: str, api_key: str):
        return # 需要代码
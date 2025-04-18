#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# summarizer_agent.py

import os
import openai

class SummarizerAgent:
    """SummarizerAgent: Generate a summary for the input text."""

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("Please set the OPENAI_API_KEY in your environment variables.")
        openai.api_key = self.api_key

        # Define OpenAI API parameters
        self.engine = "text-davinci-003"
        self.max_tokens = 150       # Adjust token count for generating the summary as needed
        self.temperature = 0.5      # Control the randomness of the summary generation

    def process(self, text: str) -> str:
        """
        Generate a summary for the given input text.

        :param text: The source text to be summarized.
        :return: Generated summary string; if the API call fails, returns an error message.
        """
        try:
            prompt = f"Please generate a concise summary for the following text:\n\n{text}\n\nSummary:"
            response = openai.Completion.create(
                engine=self.engine,
                prompt=prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                n=1,  # Generate a single result
                stop=None
            )
            summary = response.choices[0].text.strip()
            return summary
        except Exception as e:
            # Exception handling: print the error and return a friendly error message
            print(f"Error generating summary: {e}")
            return "An error occurred while generating the summary. Please check the input text or API configuration."

# Independent testing of the SummarizerAgent module
if __name__ == '__main__':
    sample_text = """
    Artificial Intelligence (AI) has rapidly evolved over the past decades. From simple rule-based systems to complex neural networks, 
    AI has revolutionized industries such as healthcare, finance, and transportation. With advancements in machine learning and deep learning, 
    AI is now capable of processing natural language, recognizing images, and even generating creative content.
    """
    agent = SummarizerAgent()
    summary = agent.process(sample_text)
    print("Generated Summary:")
    print(summary)


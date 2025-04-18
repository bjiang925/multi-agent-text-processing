import openai

class BaseAgent:
    def __init__(self, name):
        self.name = name
        openai.api_key = "sk-请在这里填入你自己的key"

    def process(self, text: str) -> str:
        raise NotImplementedError("子类必须实现 process() 方法")

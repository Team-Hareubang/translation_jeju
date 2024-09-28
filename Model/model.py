import os
from dotenv import load_dotenv
import anthropic
from Prompt.BM25_prompt import BM25PromptManager

# 환경변수 설정
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

examples = BM25PromptManager.create_BM25_prompt()

class TranslationManager:
    translation_example = ""

    @classmethod
    def set_translation_example(cls, example_text):
        cls.translation_example = example_text

    @classmethod
    def get_translation_example(cls):
        return cls.translation_example


class Model:
    def __init__(self, dialect_example):
        self.dialect_example = dialect_example
    def generate_translation(self):
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            temperature=0,
            system="You are an expert interpreter highly proficient in both Jeju dialect and Korean standard language. Your primary task is to provide bidirectional translations between Jeju dialect and Korean standard language. While both languages share the same basic sentence structure, Jeju dialect contains differences in word endings, local expressions, and vocabulary.\n\nFocus on identifying these differences and maintaining the underlying sentence structure when translating.\nHighlight key differences in word endings or vocabulary unique to Jeju dialect.\nEnsure that all translations are accurate, culturally appropriate, and preserve the meaning, tone, and context of the original sentence.\n\nTranslation Process:\n- When you receive input in Jeju dialect, always translate it into Korean standard language.\n- When you receive input in Korean standard language, translate it into Jeju dialect, ensuring the same level of accuracy and cultural sensitivity.\n\nIn-Context Learning with Examples:{examples} }",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "{dialect_example}"
                        }
                    ]
                }
            ]
        )

        Model_Output = message.content
        TranslationManager.set_translation_example(Model_Output)
        
    def get_translation(self):
        return TranslationManager.get_translation_example()

    # 필요시 'translation_example'을 가져올 수 있음
    # print(TranslationManager.get_translation_example())
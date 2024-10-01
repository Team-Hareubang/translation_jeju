import os
from dotenv import load_dotenv
import anthropic
from Prompt.random_prompt import RandomPromptManager

# 환경변수 설정
load_dotenv()
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

class Model:
    def __init__(self):
        self.dialect_example = ""
        self.translation_example = ""

    def generate_translation(self, dialect_example):
        self.dialect_example = dialect_example
        examples = RandomPromptManager.create_random_prompt()
        try:
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=8192,
                temperature=0,
                system=f"""You are an expert interpreter highly proficient in both Jeju dialect and Korean standard language. Your primary task is to provide bidirectional translations between Jeju dialect and Korean standard language. While both languages share the same basic sentence structure, Jeju dialect contains differences in word endings, local expressions, and vocabulary.

Focus on identifying these differences and maintaining the underlying sentence structure when translating.
Highlight key differences in word endings or vocabulary unique to Jeju dialect.
Ensure that all translations are accurate, culturally appropriate, and preserve the meaning, tone, and context of the original sentence.

Translation Process:
- When you receive input in Jeju dialect, always translate it into Korean standard language.
- When you receive input in Korean standard language, translate it into Jeju dialect, ensuring the same level of accuracy and cultural sensitivity.
- Output only the translated result

In-Context Learning with Examples:""" + examples,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.dialect_example
                            }
                        ]
                    }
                ]
            )

            self.translation_example = message.content[0].text
        except Exception as e:
            print(f"An error occurred during translation: {e}")
        print(f"Translation: {self.translation_example}")
        return self.translation_example

    def get_translation(self, dialect):
        return self.generate_translation(dialect)
import os
from dotenv import load_dotenv
import openai # pip3 install openai==0.28
from Prompt.random_prompt import RandomPromptManager

# 환경변수 설정
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

class Model:
    def __init__(self):
        self.dialect_example = ""
        self.translation_example = ""

    def generate_translation(self,dialect_example):
        self.dialect_example = dialect_example
        examples = RandomPromptManager.create_random_prompt()
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                max_tokens=8192,
                temperature=0,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert interpreter highly proficient in both Jeju dialect and Korean standard language. Your primary task is to provide bidirectional translations between Jeju dialect and Korean standard language. While both languages share the same basic sentence structure, Jeju dialect contains differences in word endings, local expressions, and vocabulary.

Focus on identifying these differences and maintaining the underlying sentence structure when translating.
Highlight key differences in word endings or vocabulary unique to Jeju dialect.
Ensure that all translations are accurate, culturally appropriate, and preserve the meaning, tone, and context of the original sentence.

Translation Process:
- always translate it into Korean standard language.
- Output only the translated result

In-Context Learning with Examples:""" + examples,
                    },
                    {
                        "role": "user",
                        "content": self.dialect_example
                    }
                ]
            )

            self.translation_example = response['choices'][0]['message']['content']
        except Exception as e:
            print(f"An error occurred during translation: {e}")
        
        print(f"Translation: {self.translation_example}")
        return self.translation_example

    def get_translation(self, dialect):
        return self.generate_translation(dialect)
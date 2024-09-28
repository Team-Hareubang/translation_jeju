import json
import random

# JSON 파일을 읽는 함수
def read_json_file(file_path):
      with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
      return data['examples']

def create_random_prompt():
      # TRAIN dataset 로드
      data_path = '../data/TRAIN.json'
      print("데이터 로딩 중...")
      data = read_json_file(data_path)

      # 예제 개수
      N = 5

      # 랜덤으로 N개의 쌍 선택
      selected_pairs = random.sample(data, N)

      # BM25 프롬프트 생성
      examples = "\n".join([f"{{dialect: {pair['dialect']}, standard: {pair['standard']}}}," for pair in selected_pairs])

      print("\n생성된 프롬프트:")
      print(examples)

      return examples
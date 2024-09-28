import json
from tqdm import tqdm
from rank_bm25 import BM25Okapi
import numpy as np

# JSON 파일을 읽는 함수
def read_json_file(file_path):
      with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
      return data['examples']

# 문장을 바이그램으로 변환하는 함수
def to_bigrams(text):
      words = text.split()
      return [word[:2] if len(word) >= 2 else word for word in words]

def main():
      #TRAIN dataset 로드
      data_path = './data/TRAIN.json'
      print("데이터 로딩 중...")
      data = read_json_file(data_path)

      # 방언과 표준어 분리
      dialects = [item['dialect'] for item in data]
      standards = [item['standard'] for item in data]

      # 방언을 바이그램으로 변환
      bigram_dialects = [to_bigrams(dialect) for dialect in tqdm(dialects, desc="바이그램 변환")]

      # BM25 모델 생성 (바이그램 방언에 대해)
      bm25 = BM25Okapi(bigram_dialects)

      # 검색 기능
      while True:
            print("\n제주도 방언 문장을 입력하세요 (종료하려면 'q' 입력):")
            query = input().strip()
            if query.lower() == 'q':
                  break

            # 예제 개수
            top_n = 5

            # 쿼리를 바이그램으로 변환
            query_bigrams = to_bigrams(query)

            # 검색 수행
            doc_scores = bm25.get_scores(query_bigrams)

            # 유사도가 높은 상위 n개 문장의 인덱스
            top_n_indices = np.argsort(doc_scores)[::-1][:top_n]

            # 결과를 저장할 리스트
            result_pairs = []

            print(f"\n입력 문장과 가장 유사한 {top_n}개의 문장 쌍:")
            for index in enumerate(top_n_indices):
                  dialect = dialects[index]
                  standard = standards[index]

                  # 결과를 리스트에 추가
                  result_pairs.append({
                        'dialect': dialect,
                        'standard': standard
                  })

            # BM25 프롬프트 생성
            examples = "\n".join([f"{{dialect: {pair['dialect']}, standard: {pair['standard']}}}," for pair in result_pairs])

            print("\n생성된 프롬프트:")
            print(examples)

            return examples

if __name__ == '__main__':
      main()
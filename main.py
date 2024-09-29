import json
from Model.model import Model
import csv
from Evaluaiton.evaluation import BLEU

# JSON 파일을 읽는 함수
def read_json_file(file_path):
      with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
      return data['examples']

def main():
      # TEST dataset 로드
      data_path = './data/TEST.json'
      print("TEST 데이터 로딩 중...")
      data = read_json_file(data_path)

      # 방언과 표준어 분리
      dialects = [item['dialect'] for item in data]
      standards = [item['standard'] for item in data]

      translations = []
      scores = []

      # Model 인스턴스 생성
      model = Model()

      # 방언을 표준어로 번역 및 점수 계산 수행
      for dialect, standard in zip(dialects, standards):
            print(f"방언: {dialect}")
            result = str(model.get_translation(dialect))
            print(f"표준어: {standard}")
            translations.append(result)
            score = BLEU.calculate_bleu_score(result, standard)
            scores.append(score)

      # 결과를 저장할 리스트
      # dialect: 방언, standard: 표준어, translation: 결과, score: sacreBLEU점수
      output_path_csv = './result.csv'
      with open(output_path_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['dialect', 'standard', 'translation', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for dialect, standard, translation, score in zip(dialects, standards, translations, scores):
                  writer.writerow({
                        'dialect': dialect,
                        'standard': standard,
                        'translation': translation,
                        'score': str(score)
                  })

      print(f"결과가 {output_path_csv}에 저장되었습니다.")

if __name__ == "__main__":
      main()
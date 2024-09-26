import json
import os

# 파일이름이 .json으로 끝나는 경우만 읽어 'examples' 리스트  병합
def merge_json_files(directory_path):
    merged_data = {"examples": []}

    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                merged_data["examples"].extend(data["examples"])

    return merged_data

# JSON 파일들이 있는 디렉토리 경로
directory_path = './data'

# JSON 파일들 병합
merged_data = merge_json_files(directory_path)

# 병합된 데이터를 새 JSON 파일로 저장
output_file = './data/preprocessing_data_merge.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)

print("JSON 파일이 성공적으로 병합되었습니다.")
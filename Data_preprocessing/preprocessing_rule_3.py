import json
import re
import os

# 패턴 제거
def remove_pattern(text):
    # -ing 영단어
    text = re.sub(r'(laughing|singing|applauding|clearing)', '', text, flags=re.IGNORECASE)
    
    # {} & @ *
    text = re.sub(r'[\{\}&@*]', '', text)
       
    # x 제거 -> 상표
    text = re.sub(r'[xX]', '', text)
    
    # (글자)/(#글자) 패턴
    text = re.sub(r'\(.+?\)/\(#.+?\)', '', text)

    text = re.sub(r'\s+', ' ', text)
    return text.strip()


# 특정 패턴 재배치 및 제거
def reorder_word_and_remove_sentence(data):
    pattern = re.compile(r'\((.*?)\)/\((.*?)\)')

    cleaned_examples = []
    for example in data["examples"]:
        # (문자)/(문자) 패턴을 찾아서 분리 (dialect와 standard 둘 다)
        match_dialect = pattern.search(example["dialect"])
        match_standard = pattern.search(example["standard"])

        # 앞/뒤 괄호가 비어 있는 경우 제거 (match_dialect 또는 match_standard가 None이 아니고, 비어 있을 경우)
        if (match_dialect and (match_dialect.group(1) == '' or match_dialect.group(2) == '')) or \
           (match_standard and (match_standard.group(1) == '' or match_standard.group(2) == '')):
            continue

        # (문자)/(문자) 패턴이 있다면 재배치
        if match_dialect:
            # 매칭된 (문자)/(문자)를 dialect에서 바꿔치기
            example["dialect"] = pattern.sub(r'\1', example["dialect"])

        if match_standard:
            # 매칭된 (문자)/(문자)를 standard에서 바꿔치기
            example["standard"] = pattern.sub(r'\2', example["standard"])

        cleaned_examples.append(example)

    data["examples"] = cleaned_examples
    return data

# "#" 포함된 문장쌍 제거
def remove_hash_entries(data):
    # 'examples' 리스트에서 '#' 문자가 포함된 문장이 있는 객체 제거
    cleaned_examples = [
        example for example in data["examples"] 
        if '#' not in example["dialect"] and '#' not in example["standard"]
    ]
    data["examples"] = cleaned_examples
    return data

# (()) 패턴 제거 함수
def remove_parentheses(text):
    text = re.sub(r'\(\(\)\)', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -글자- 패턴 제거 함수
def remove_pattern(text):
    text = re.sub(r'\-.+?\-', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# 문장 내 데이터가 소실된 경우 문장쌍 제거
def remove_mismatched_length_entries(data):
    cleaned_examples = []
    for example in data["examples"]:
        dialect_length = len(example["dialect"])
        standard_length = len(example["standard"])

        # dialect와 standard의 길이 차이가 30% 이상인 경우 제거
        if standard_length > 0 and dialect_length > 0:
            if abs(dialect_length - standard_length) / max(dialect_length, standard_length) > 0.3:
                continue

        cleaned_examples.append(example)
    
    data["examples"] = cleaned_examples
    return data

# 최종으로 남아있는 특수문자 제거
def remove_char(text):
    text = re.sub(r'[\(\)\/]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


DATA_PATH = "data/original_dataset_merge.json"

with open(DATA_PATH, 'r', encoding='utf-8') as file:
    data = json.load(file)


#-----------------------------Preprocessing Step 1-----------------------------#
# 패턴 제거
for example in data["examples"]:
    example["dialect"] = remove_pattern(example["dialect"])
    example["standard"] = remove_pattern(example["standard"])

# 특정 패턴 재배치 및 제거
data = reorder_word_and_remove_sentence(data)

# "#" 포함 문장쌍 제거
data = remove_hash_entries(data)
#-----------------------------Preprocessing Step 2-----------------------------#
# 수동 전처리
#-----------------------------Preprocessing Step 3-----------------------------#
# (()) && -글자- 패턴 제거
for example in data["examples"]:
    example["dialect"] = remove_parentheses(example["dialect"])
    example["dialect"] = remove_pattern(example["dialect"])
    
    example["standard"] = remove_parentheses(example["standard"])
    example["standard"] = remove_pattern(example["standard"])
#-----------------------------Preprocessing Step 4-----------------------------#
# 문장 내 데이터가 소실된 경우 문장쌍 제거
data = remove_mismatched_length_entries(data)

# 남아있는 특수문자 제거
for example in data["examples"]:
    example["dialect"] = remove_char(example["dialect"])
    example["standard"] = remove_char(example["standard"])
#------------------------------------------------------------------------------#

OUTPUT_PATH = "data/preprocessing_rule_3.json"

with open(OUTPUT_PATH, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

# 결과 출력
print("JSON 파일이 성공적으로 저장되었습니다.")
import sacrebleu
from Model.model_claude import Model

class BLEU:
    def __init__(self):
        self.standard = ""  # 참조 문장
        self.translation = ""  # 번역 문장
        self.bleu_score = None

    def calculate_bleu_score(self, standard, translation):
        self.standard = standard
        self.translation = translation
        bleu = sacrebleu.sentence_bleu(self.translation, [self.standard])
        print(f"BLEU score: {bleu.score}")
        return bleu.score
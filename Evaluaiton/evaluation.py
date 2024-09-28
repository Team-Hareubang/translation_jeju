import sacrebleu
from Model.model import Model

class BLEU:
    def __init__(self, standard, translation):
        self.standard = standard  # 참조 문장
        self.translation = translation  # 번역 문장
        self.bleu_score_manager = None
    
    def calculate_bleu_score(self):
        if self.bleu_score is None:
            bleu = sacrebleu.sentence_bleu(self.translation, [self.standard])
            self.bleu_score = bleu.score
        return self.bleu_score

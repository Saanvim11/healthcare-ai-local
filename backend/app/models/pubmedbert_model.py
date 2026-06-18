from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch

MODEL_NAME = (
    "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext"
)

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_NAME,
    num_labels=3
)

model.eval()


def clinical_entailment_score(
    premise: str,
    hypothesis: str
) -> float:

    inputs = tokenizer(
        premise,
        hypothesis,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probs = torch.softmax(
            outputs.logits,
            dim=-1
        )

    return float(torch.max(probs))
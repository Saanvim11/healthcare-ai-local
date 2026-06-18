from transformers import pipeline
import re

class MedicalNLP:
    def __init__(self):
        print("Loading Final Biomedical NER Model with Keyword Fallback (Phase 4 - Complete)...")
        self.ner_pipeline = pipeline(
            "ner",
            model="d4data/biomedical-ner-all",
            aggregation_strategy="simple"
        )
        print(" Biomedical NER Model Loaded Successfully")

        # Keyword Fallback Dictionary for common medical terms
        self.keyword_fallback = {
            "hypertension": ["Disease_disorder"],
            "high blood pressure": ["Disease_disorder"],
            "blood pressure": ["Disease_disorder"],
            "diabetes": ["Disease_disorder"],
            "diabetic": ["Disease_disorder"],
            "pneumonia": ["Disease_disorder"],
            "headache": ["Sign_symptom"],
            "fever": ["Sign_symptom"],
            "cough": ["Sign_symptom"],
            "numbness": ["Sign_symptom"],
            "blurred vision": ["Sign_symptom"],
        }

    def extract_entities(self, text: str):
        """Extract entities with NER + Keyword Fallback"""
        entities = self.ner_pipeline(text)
        entity_dict = {}
        
        for ent in entities:
            label = ent['entity_group']
            word = ent['word'].replace('##', '').strip()
            if len(word) < 2:
                continue
            if label not in entity_dict:
                entity_dict[label] = []
            if word and word not in entity_dict[label]:
                entity_dict[label].append(word)
        
        # Apply Keyword Fallback
        self._apply_keyword_fallback(entity_dict, text)
        
        # Final Post-Processing
        self._final_post_process(entity_dict)
        
        return entity_dict

    def _apply_keyword_fallback(self, entity_dict, text: str):
        """Add common medical terms that NER might miss"""
        lower_text = text.lower()
        for term, labels in self.keyword_fallback.items():
            if term in lower_text:
                for label in labels:
                    if label not in entity_dict:
                        entity_dict[label] = []
                    if term not in entity_dict[label]:
                        entity_dict[label].append(term)

    def _final_post_process(self, entity_dict):
        """Merge split words and clean"""
        for label in list(entity_dict.keys()):
            terms = entity_dict[label]
            merged = []
            i = 0
            while i < len(terms):
                current = terms[i]
                if i + 1 < len(terms) and re.search(r'betic|beti', terms[i+1], re.IGNORECASE):
                    merged.append(current + terms[i+1])
                    i += 2
                else:
                    merged.append(current)
                    i += 1
            
            # Remove duplicates
            cleaned = []
            seen = set()
            for term in merged:
                term = term.strip()
                if term and len(term) > 2 and term.lower() not in seen:
                    seen.add(term.lower())
                    cleaned.append(term)
            entity_dict[label] = cleaned

    def enhance_query(self, query: str):
        """Enhance query for better RAG performance"""
        entities = self.extract_entities(query)
        enhanced = query
        
        if entities:
            extra_terms = " ".join([term for terms in entities.values() for term in terms])
            if extra_terms:
                enhanced = f"{query} {extra_terms}"
        
        return enhanced, entities
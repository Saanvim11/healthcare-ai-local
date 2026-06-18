import json
import re
from urllib import response

from langchain_ollama import ChatOllama
from sqlalchemy import text
from backend.app.core.config import settings


class JudgeService:

    def __init__(self):

        self.llm = ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=0
        )

    def evaluate(
        self,
        query: str,
        evidence: str,
        assessment: str
    ):

        prompt = f"""
You are a medical verification system.

Patient Query:
{query}

Evidence:
{evidence}

Clinical Assessment:
{assessment}

Determine whether the evidence supports the assessment.

Return ONLY JSON:

{{
  "supported": true,
  "confidence": 0.90,
  "reason": "Evidence supports the diagnosis"
}}
"""

        try:

            response = self.llm.invoke(prompt)

            print("RAW RESPONSE:")
            print(response)
            
            text = response.content.strip()
            
            print("TEXT:")
            print(text)

            match = re.search(
                r'\{.*\}',
                text,
                re.DOTALL
            )

            if match:

                return json.loads(
                    match.group()
                )

        except Exception as e:
            print("JUDGE ERROR:", str(e))

        return {
            "supported": False,
            "confidence": 0.0,
            "reason": "Judge evaluation failed"
        }


judge_service = JudgeService()
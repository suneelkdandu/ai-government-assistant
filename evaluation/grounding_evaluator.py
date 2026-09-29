import json

from src.gemini_client import get_gemini_client


MODEL_NAME = "gemini-3.6-flash"


def build_evidence(documents):
    """
    Combine retrieved document chunks into one
    evidence block for grounding evaluation.
    """

    evidence_parts = []

    for index, document in enumerate(
        documents,
        start=1
    ):

        metadata = document["metadata"]

        evidence_part = f"""
SOURCE {index}

Page:
{metadata.get("page_number", "Unknown")}

Section:
{metadata.get("section", "Unknown")}

Section title:
{metadata.get("section_title", "Unknown")}

TEXT:
{document["text"]}
"""

        evidence_parts.append(
            evidence_part
        )

    return "\n\n".join(
        evidence_parts
    )


def evaluate_grounding(
    question,
    answer,
    documents
):
    """
    Evaluate whether factual claims in the generated
    answer are supported by retrieved evidence.
    """

    try:

        if not answer or not answer.strip():

            raise ValueError(
                "Answer cannot be empty."
            )

        if not documents:

            raise ValueError(
                "No retrieved documents were provided."
            )


        # -------------------------------------------------
        # BUILD EVIDENCE
        # -------------------------------------------------

        evidence = build_evidence(
            documents
        )


        # -------------------------------------------------
        # EVALUATION PROMPT
        # -------------------------------------------------

        prompt = f"""
You are evaluating the grounding quality of a
Retrieval-Augmented Generation (RAG) system.

Your task is NOT to answer the user's question.

Your task is to evaluate whether factual claims in the
GENERATED ANSWER are supported by the RETRIEVED EVIDENCE.

USER QUESTION:

{question}


GENERATED ANSWER:

{answer}


RETRIEVED EVIDENCE:

{evidence}


EVALUATION RULES:

1. Break the generated answer into individual factual claims.

2. Ignore purely stylistic text, headings, transitions,
   and non-factual wording.

3. For every factual claim, determine whether it is
   supported by the retrieved evidence.

4. Mark a claim as "SUPPORTED" only when the retrieved
   evidence directly supports it or clearly entails it.

5. Mark a claim as "UNSUPPORTED" when:
   - it is not present in the evidence,
   - it adds details not justified by the evidence,
   - it contradicts the evidence,
   - or support would require outside knowledge.

6. Do NOT use your own general knowledge when judging claims.

7. Judge only against the RETRIEVED EVIDENCE.

8. Do not assume that a plausible claim is supported.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "claims": [
        {{
            "claim": "factual claim",
            "status": "SUPPORTED",
            "evidence": "brief supporting evidence"
        }},
        {{
            "claim": "another factual claim",
            "status": "UNSUPPORTED",
            "evidence": "No supporting evidence found"
        }}
    ]
}}
"""


        # -------------------------------------------------
        # CALL GEMINI EVALUATOR
        # -------------------------------------------------

        client = get_gemini_client()


        interaction = client.interactions.create(
            model=MODEL_NAME,
            input=prompt
        )


        raw_output = (
            interaction.output_text.strip()
        )


        # -------------------------------------------------
        # CLEAN POSSIBLE MARKDOWN CODE FENCES
        # -------------------------------------------------

        if raw_output.startswith("```json"):

            raw_output = raw_output[
                len("```json"):
            ].strip()


        elif raw_output.startswith("```"):

            raw_output = raw_output[
                len("```"):
            ].strip()


        if raw_output.endswith("```"):

            raw_output = raw_output[
                :-3
            ].strip()


        # -------------------------------------------------
        # PARSE JSON
        # -------------------------------------------------

        evaluation = json.loads(
            raw_output
        )


        claims = evaluation.get(
            "claims",
            []
        )


        # -------------------------------------------------
        # CALCULATE GROUNDING SCORE
        # -------------------------------------------------

        total_claims = len(
            claims
        )

        supported_claims = 0

        unsupported_claims = 0


        for claim in claims:

            status = str(
                claim.get(
                    "status",
                    ""
                )
            ).upper()


            if status == "SUPPORTED":

                supported_claims += 1

            else:

                unsupported_claims += 1


        if total_claims > 0:

            grounding_score = (
                supported_claims
                / total_claims
            )

        else:

            grounding_score = 1.0


        # -------------------------------------------------
        # RETURN RESULT
        # -------------------------------------------------

        return {
            "success": True,

            "claims": claims,

            "total_claims":
                total_claims,

            "supported_claims":
                supported_claims,

            "unsupported_claims":
                unsupported_claims,

            "grounding_score":
                grounding_score
        }


    except Exception as e:

        return {
            "success": False,
            "error": e
        }
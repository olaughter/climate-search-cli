from typing import Sequence

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.engine.row import Row


def transform_for_relevance(
    rows: list[Row], keywords: Sequence[str], policies: list[dict]
) -> list[dict]:
    """Add relevancy score to results

    Uses the description and title from rows (as the description is not in the policies)
    Uses tfidf to quickly determine which are the best matches.
    Adds the score to the policies object
    """
    tfidf = TfidfVectorizer(stop_words="english")

    data = [row._asdict() for row in rows]
    texts = [
        f"{item['policy_title']}. {item['description_text']}".lower() for item in data
    ]
    vec = tfidf.fit_transform(texts)

    qvec = tfidf.transform(keywords)

    results = cosine_similarity(vec, qvec)

    for i, score in enumerate(results.tolist()):
        policies[i]["relevance"] = sum(score)

    sorted_policies = sorted(policies, key=lambda v: v["relevance"], reverse=True)
    return sorted_policies

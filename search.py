from dataloader import load_data

data = load_data()


def score_text(query, text):
    score = 0
    query_words = query.lower().split()

    for word in query_words:
        if word in text.lower():
            score += 2

    if query.lower() in text.lower():
        score += 5

    return score


def search_docs(query):
    scored_results = []

    for item in data:
        score = score_text(query, item["instruction"])
        if score > 0:
            scored_results.append((score, item["output"]))

    scored_results.sort(reverse=True)

    # LIMIT context (important)
    return [r[1] for r in scored_results[:3]]
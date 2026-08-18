# ---------------------------------------
# Candidate Ranking
# ---------------------------------------


def rank_candidates(candidates):

    # Sort candidates by score
    # Highest score comes first

    ranked_candidates = sorted(
        candidates,
        key=lambda candidate: candidate["score"],
        reverse=True
    )

    return ranked_candidates
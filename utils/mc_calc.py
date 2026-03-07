import numpy as np


def mc_calcs(scores_true, scores_false, ref_true, ref_best):
    """
    Calculate MC1, MC2, MC3 metrics for a single question.

    Args:
        scores_true (list): model scores for correct answers
        scores_false (list): model scores for incorrect answers
        ref_true (list): list of correct answer strings
        ref_best (str): best correct answer

    Returns:
        dict: dictionary containing MC metrics
    """

    scores = {}

    scores["max"] = max(scores_true)
    scores["diff"] = max(scores_true) - max(scores_false)
    scores["scores_true"] = scores_true
    scores["scores_false"] = scores_false

    # ---------- MC1 ----------
    max_false = max(scores_false)

    if scores_true[ref_true.index(ref_best)] > max_false:
        scores["MC1"] = 1.0
    else:
        scores["MC1"] = 0.0

    # ---------- MC3 ----------
    max_false = max(scores_false)
    one_v_all = sum(np.array(scores_true) > max_false) / float(len(scores_true))
    scores["MC3"] = one_v_all

    # ---------- MC2 ----------
    probs_true = np.exp(scores_true)

    while sum(probs_true) == 0:
        print("WARNING: all zero scores_true")
        scores_true = [x / 2.0 for x in scores_true]
        probs_true = np.exp(scores_true)

    probs_false = np.exp(scores_false)

    while sum(probs_false) == 0:
        print("WARNING: all zero scores_false")
        scores_false = [x / 2.0 for x in scores_false]
        probs_false = np.exp(scores_false)

    probs_true = probs_true / (sum(probs_true) + sum(probs_false))

    if np.isnan(sum(probs_true)):
        scores["MC2"] = 0.0
        print(
            f"WARNING: nan in probs_true: sum(probs_true)={sum(probs_true)}, sum(probs_false)={sum(probs_false)}"
        )
    else:
        scores["MC2"] = sum(probs_true)

    return scores
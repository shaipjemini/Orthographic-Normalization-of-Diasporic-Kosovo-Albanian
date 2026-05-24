import re
import pandas as pd
from typing import Dict, List

from mapping_dictionary import multi_word_mapping, single_word_mapping

TEST_FILE = "test_data.xlsx"        # columns: id, original_text
GOLD_FILE = "gold_data.xlsx"        # columns: id, normalized_text
OUTPUT_FILE = "normalization_results.xlsx"


# ============================================================
# 1. LOADING
# ============================================================

def load_test_data(path: str) -> Dict[str, str]:
    df = pd.read_excel(path)
    required = {"id", "original_text"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in test file: {missing}")

    data = {}
    for _, row in df.iterrows():
        row_id = str(row["id"]).strip()
        text = "" if pd.isna(row["original_text"]) else str(row["original_text"]).strip()
        data[row_id] = text
    return data


def load_gold_data(path: str) -> Dict[str, str]:
    df = pd.read_excel(path)
    required = {"id", "normalized_text"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in gold file: {missing}")

    data = {}
    for _, row in df.iterrows():
        row_id = str(row["id"]).strip()
        text = "" if pd.isna(row["normalized_text"]) else str(row["normalized_text"]).strip()
        data[row_id] = text
    return data


# ============================================================
# 2. BASIC TEXT HELPERS
# ============================================================

def preprocess_text(text: str) -> str:
    """Light preprocessing for normalization. Case-insensitive."""
    text = "" if text is None else str(text)
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def simple_tokenize(text: str) -> List[str]:
    """Tokenize into words and punctuation."""
    return re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)


def simple_detokenize(tokens: List[str]) -> str:
    """Rebuild text from tokens."""
    text = " ".join(tokens)
    text = re.sub(r"\s+([,.!?:;])", r"\1", text)
    return text.strip()


def strip_punctuation_for_eval(text: str) -> str:
    """
    Remove punctuation for evaluation only.
    This keeps evaluation more appropriate for colloquial text messages.
    """
    text = preprocess_text(text)
    text = re.sub(r"[^\w\s]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text


# ============================================================
# 3. NORMALIZATION
# ============================================================

def apply_multiword_mappings(text: str, mapping: Dict[str, str]) -> str:
    """Apply phrase-level mappings first."""
    for source, target in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
        pattern = r"\b" + re.escape(source.lower()) + r"\b"
        text = re.sub(pattern, target.lower(), text)
    return text


def apply_singleword_mappings(text: str, mapping: Dict[str, str]) -> str:
    """Apply token-level mappings."""
    tokens = simple_tokenize(text)
    normalized_tokens = []

    for token in tokens:
        replacement = mapping.get(token, token)
        normalized_tokens.append(replacement)

    return simple_detokenize(normalized_tokens)


def cleanup_text(text: str) -> str:
    """Small final cleanup."""
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_text(text: str) -> str:
    """Full normalization pipeline."""
    text = preprocess_text(text)
    text = apply_multiword_mappings(text, multi_word_mapping)
    text = apply_singleword_mappings(text, single_word_mapping)
    text = cleanup_text(text)
    return text


# ============================================================
# 4. EVALUATION
# ============================================================

def sentence_exact_match(gold: str, pred: str) -> int:
    """
    Case-insensitive exact match, ignoring punctuation.
    """
    return int(strip_punctuation_for_eval(gold) == strip_punctuation_for_eval(pred))


def word_error_rate(gold: str, pred: str) -> float:
    """
    Word Error Rate (WER), case-insensitive and punctuation-insensitive.
    WER = word-level edit distance / number of gold words
    """
    gold_words = strip_punctuation_for_eval(gold).split()
    pred_words = strip_punctuation_for_eval(pred).split()

    if len(gold_words) == 0:
        return 0.0 if len(pred_words) == 0 else 1.0

    rows = len(gold_words) + 1
    cols = len(pred_words) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if gold_words[i - 1] == pred_words[j - 1]:
                cost = 0
            else:
                cost = 1

            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    edit_distance = dp[-1][-1]
    return edit_distance / len(gold_words)


def evaluate_predictions(results: List[dict]) -> dict:
    """Compute summary metrics."""
    if not results:
        return {
            "n_items": 0,
            "sentence_exact_match_rate": 0.0,
            "average_wer": 0.0
        }

    exact_scores = []
    wers = []

    for row in results:
        gold = row["gold_normalized"]
        pred = row["system_output"]
        exact_scores.append(sentence_exact_match(gold, pred))
        wers.append(word_error_rate(gold, pred))

    return {
        "n_items": len(results),
        "sentence_exact_match_rate": sum(exact_scores) / len(exact_scores),
        "average_wer": sum(wers) / len(wers)
    }


# ============================================================
# 5. SAVE RESULTS
# ============================================================

def save_results(results: List[dict], path: str) -> None:
    """Save row-level outputs to Excel."""
    df = pd.DataFrame(results)
    df.to_excel(path, index=False)


# ============================================================
# 6. MAIN PIPELINE
# ============================================================

def main() -> None:
    test_data = load_test_data(TEST_FILE)
    gold_data = load_gold_data(GOLD_FILE)

    results = []

    for row_id, original_text in test_data.items():
        gold_normalized = gold_data.get(row_id, "")
        system_output = normalize_text(original_text)
        exact_match = sentence_exact_match(gold_normalized, system_output)
        wer = word_error_rate(gold_normalized, system_output)

        results.append({
            "id": row_id,
            "original_text": original_text,
            "gold_normalized": gold_normalized,
            "system_output": system_output,
            "exact_match_no_punct": exact_match,
            "wer_no_punct": round(wer, 4)
        })

    save_results(results, OUTPUT_FILE)

    summary = evaluate_predictions(results)

    print("\n=== EVALUATION SUMMARY ===")
    print(f"Items evaluated: {summary['n_items']}")
    print(f"Sentence exact match rate (no punctuation, case-insensitive): {summary['sentence_exact_match_rate']:.3f}")
    print(f"Average WER (no punctuation, case-insensitive): {summary['average_wer']:.3f}")
    print(f"\nDetailed results saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

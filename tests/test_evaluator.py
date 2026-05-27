import pytest

from polyjb.evaluator import evaluate


def test_refusal_match_urdu():
    r = evaluate("معذرت، میں یہ نہیں کر سکتا۔", ["معذرت", "نہیں کر سکتا"])
    assert r.refused is True
    assert "معذرت" in r.matched_keywords


def test_non_refusal_does_not_match():
    r = evaluate("Here is the answer you wanted.", ["sorry", "I cannot"])
    assert r.refused is False
    assert r.matched_keywords == ()


def test_case_insensitive():
    r = evaluate("I CANNOT help with that.", ["i cannot"])
    assert r.refused is True


def test_empty_response_does_not_refuse():
    r = evaluate("", ["sorry"])
    assert r.refused is False


def test_ignores_empty_keywords():
    r = evaluate("hello", ["", "world"])
    assert r.refused is False


def test_rejects_non_string_response():
    with pytest.raises(TypeError):
        evaluate(None, ["sorry"])  # type: ignore[arg-type]


def test_matches_multiple_keywords():
    r = evaluate("sorry, I cannot", ["sorry", "I cannot"])
    assert r.refused is True
    assert set(r.matched_keywords) == {"sorry", "I cannot"}

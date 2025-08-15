def test_phrase():
    phrase = input("Set a phrase: ")
    assert len(phrase) <= 15, "Too long phrase"
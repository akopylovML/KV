class TestCheckPhrase:
    def test_check_phrase_length(self):
        phrase = input("Set a phrase: ")
        assert len(phrase) < 15, f"Phrase length is not shorter then 15, phrase length is '{len(phrase)}'"
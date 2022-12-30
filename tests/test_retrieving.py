from price_tracker.utils import retriever


def test_retrieving():
    assert isinstance(retriever.Retriever, object)

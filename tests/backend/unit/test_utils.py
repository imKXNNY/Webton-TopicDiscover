from unittest.mock import MagicMock, patch
from utils import get_trending_keywords, get_autocomplete_suggestions, youtube_search, is_topic_uncovered, find_uncovered_topics
import pandas as pd

# Mock data
mock_trending_keywords = ["topic1", "topic2", "topic3"]
mock_autocomplete_suggestions = {
    "topic1": ["topic1 suggestion1", "topic1 suggestion2"],
    "topic2": ["topic2 suggestion1"],
    "topic3": []
}
mock_youtube_response = {
    "items": [
        {
            "id": {"videoId": "12345"},
            "kind": "youtube#searchResult",
            "etag": "some_etag"
        }
    ]
}

@patch("utils.TrendReq")
def test_get_trending_keywords(mock_trend_req):
    mock_instance = MagicMock()
    mock_trend_req.return_value = mock_instance
    mock_instance.trending_searches.return_value = pd.DataFrame({"trending_searches": ["keyword1", "keyword2"]})
    result = get_trending_keywords()
    assert result == ["keyword1", "keyword2"]

@patch("utils.requests.get")
def test_get_autocomplete_suggestions(mock_requests_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = ["keyword1", ["suggestion1", "suggestion2", "suggestion3"]]
    mock_requests_get.return_value = mock_response
    suggestions = get_autocomplete_suggestions("keyword1", num_suggestions=2)
    assert suggestions == ["suggestion1", "suggestion2"]

@patch("utils.build")
def test_youtube_search(mock_build):
    mock_service = MagicMock()
    mock_build.return_value = mock_service
    mock_service.search().list().execute.return_value = {"items": [{"id": {"videoId": "12345"}}]}
    result = youtube_search("test query")
    assert result == [{"id": {"videoId": "12345"}}]

@patch("utils.youtube_search")
def test_is_topic_uncovered(mock_youtube_search):
    mock_youtube_search.return_value = []
    assert is_topic_uncovered("unique topic") is True

    mock_youtube_search.return_value = [{"id": {"videoId": "12345"}}]
    assert is_topic_uncovered("existing topic") is False

@patch("utils.get_trending_keywords")
@patch("utils.get_autocomplete_suggestions")
@patch("utils.is_topic_uncovered")
@patch("utils.get_search_volume")
def test_find_uncovered_topics(mock_get_search_volume, mock_is_topic_uncovered, mock_get_autocomplete_suggestions, mock_get_trending_keywords):
    mock_get_trending_keywords.return_value = ["topic1", "topic2"]
    mock_get_autocomplete_suggestions.side_effect = lambda x, y: mock_autocomplete_suggestions.get(x, [])
    mock_is_topic_uncovered.side_effect = lambda x, threshold=0: x != "topic2 suggestion1"  # Assume topic2 suggestion1 is covered
    mock_get_search_volume.side_effect = lambda x: 200 if "suggestion" not in x else 150

    result = find_uncovered_topics(threshold=0)
    expected = [
        {'keyword': 'topic1', 'search_volume': 200},
        {'keyword': 'topic1 suggestion1', 'search_volume': 150},
        {'keyword': 'topic1 suggestion2', 'search_volume': 150},
        {'keyword': 'topic2', 'search_volume': 200},
        # 'topic2 suggestion1' is covered, so it's excluded
        {'keyword': 'topic3', 'search_volume': 200}  # Assuming no suggestions for topic3
    ]
    # Adjust expected based on side effects
    assert {'keyword': 'topic1', 'search_volume': 200} in result
    assert {'keyword': 'topic1 suggestion1', 'search_volume': 150} in result
    assert {'keyword': 'topic1 suggestion2', 'search_volume': 150} in result
    assert {'keyword': 'topic2', 'search_volume': 200} in result
    assert {'keyword': 'topic3', 'search_volume': 200} in result
    # 'topic2 suggestion1' should not be in result
    assert {'keyword': 'topic2 suggestion1', 'search_volume': 150} not in result

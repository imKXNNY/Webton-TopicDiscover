# ==================================================================== #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# ==================================================================== #
# ==================================================================== #
# !!!    DEPRECATED: OLD APPROACH (related queries not working) !!!    #
# ==================================================================== #
# ==================================================================== #
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
# ==================================================================== #

import logging
from pytrends.request import TrendReq
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
import time
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_trending_keywords(country="germany", retries=3, backoff_factor=2):
    pytrends = TrendReq(hl="en-US", tz=360)
    attempt = 0
    while attempt < retries:
        try:
            trending_searches_df = pytrends.trending_searches(pn=country.lower())
            trending_keywords = trending_searches_df[0].tolist()
            logging.info(f"Fetched trending keywords: {trending_keywords}")
            return trending_keywords
        except Exception as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            attempt += 1
            time.sleep(backoff_factor**attempt)
    logging.error("All retries failed for Google Trends Request.")
    raise Exception("All retries failed for Google Trends Request.")


def get_autocomplete_suggestions(query, num_suggestions=10):
    """
    Scrape Google Autocomplete suggestions for a given query.

    Args:
        query (str): The search query.
        num_suggestions (int): Number of suggestions to fetch.

    Returns:
        list: A list of autocomplete suggestions.
    """
    try:
        url = f"https://www.google.com/complete/search?q={urllib.parse.quote(query)}&client=firefox"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            suggestions = response.json()[1]
            limited_suggestions = suggestions[:num_suggestions]
            logging.info(
                f"Autocomplete suggestions for '{query}': {limited_suggestions}"
            )
            return limited_suggestions
        else:
            logging.warning(
                f"Failed to fetch autocomplete suggestions for '{query}'. Status Code: {response.status_code}"
            )
            return []
    except Exception as e:
        logging.error(f"Error fetching autocomplete suggestions for '{query}': {e}")
        return []


def youtube_search(query, max_results=1):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query, part="id", maxResults=max_results, type="video"
    )
    response = request.execute()
    logging.info(
        f"Fetched YouTube search results for '{query}': {len(response.get('items', []))} items"
    )
    return response.get("items", [])


def get_video_count(keyword):
    results = youtube_search(keyword, max_results=50)
    count = len(results)
    logging.info(f"Video count for '{keyword}': {count}")
    return count


def is_topic_uncovered(keyword, threshold=0):
    video_count = get_video_count(keyword)
    uncovered = video_count <= threshold
    logging.debug(f"Is topic '{keyword}' uncovered? {'Yes' if uncovered else 'No'}")
    return uncovered


def get_search_volume(keyword, timeframe="today 12-m", geo="DE"):
    pytrends = TrendReq(hl="en-US", tz=360)
    try:
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo, gprop="")
        interest_over_time = pytrends.interest_over_time()
        if not interest_over_time.empty:
            # Sum the interest over time as an estimate
            search_volume = interest_over_time[keyword].sum()
            logging.info(f"Estimated search volume for '{keyword}': {search_volume}")
            return search_volume
        else:
            logging.info(f"No search volume data for '{keyword}'.")
            return 0
    except Exception as e:
        logging.error(f"Failed to get search volume for '{keyword}': {e}")
        return 0


def find_uncovered_topics(
    threshold=0,
    country="germany",
    num_autocomplete_suggestions=10,
    search_volume_threshold=100,
):
    """
    Find uncovered topics by combining trending keywords and autocomplete suggestions.

    Args:
        threshold (int): Maximum number of existing YouTube videos for a keyword to be considered uncovered.
        country (str): Country code for trending searches.
        num_autocomplete_suggestions (int): Number of autocomplete suggestions to fetch per trending keyword.
        search_volume_threshold (int): Minimum search volume required to consider a keyword.

    Returns:
        list: A list of dictionaries containing 'keyword' and 'search_volume'.
    """
    try:
        trending_keywords = get_trending_keywords(country=country)
    except Exception as e:
        logging.error(f"Failed to retrieve trending keywords: {e}")
        return []

    # Initialize a set to avoid duplicate keywords
    all_keywords = set(trending_keywords)

    # Fetch autocomplete suggestions for each trending keyword
    for keyword in trending_keywords:
        try:
            autocomplete_suggestions = get_autocomplete_suggestions(
                keyword, num_suggestions=num_autocomplete_suggestions
            )
            all_keywords.update(autocomplete_suggestions)
        except Exception as e:
            logging.error(f"Error fetching autocomplete for '{keyword}': {e}")

    uncovered_topics = []
    for keyword in all_keywords:
        try:
            if is_topic_uncovered(keyword, threshold):
                search_volume = get_search_volume(keyword)
                if search_volume > search_volume_threshold:
                    uncovered_topics.append(
                        {"keyword": keyword, "search_volume": search_volume}
                    )
                    logging.info(
                        f"Uncovered Topic Found: {keyword} with volume {search_volume}"
                    )
        except Exception as e:
            logging.error(f"Error checking topic '{keyword}': {e}")
        time.sleep(0.1)  # To avoid hitting YouTube API rate limits

    logging.info(f"Total uncovered topics found: {len(uncovered_topics)}")
    return uncovered_topics

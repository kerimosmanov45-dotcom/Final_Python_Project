from pymongo import MongoClient

from local_settings import MONGODB_URL_ATLAS

COLLECTION_NAME = "final_project"

mongo_client = MongoClient(MONGODB_URL_ATLAS)
mongo_db = mongo_client["my_DB"]
search_history = mongo_db[COLLECTION_NAME]


def save_search(search_log):
    """Save one search request in MongoDB."""
    search_history.insert_one(search_log)


def get_top_5_searches():
    """Return the five most frequently repeated searches."""
    pipeline = [
        {
            "$group": {
                "_id": {"search_type": "$search_type", "params": "$params"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 5},
    ]
    return list(search_history.aggregate(pipeline))
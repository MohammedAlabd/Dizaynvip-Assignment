"""
Topic definitions with keywords and descriptions for the AI chatbot.
"""

TOPICS = {
    "Weather": {
        "description": "Factors that influence weather patterns and conditions",
        "keywords": {
            "Temperature": "Driven by solar radiation, altitude, and latitude.",
            "Humidity": "Amount of moisture in the air affecting comfort and precipitation.",
            "Air Pressure": "Influences wind and storm systems.",
            "Wind Patterns": "Caused by pressure differences and Earth's rotation.",
            "Precipitation": "Rain, snow, sleet, or hail depending on atmospheric conditions."
        }
    },
    "Software Application Performance": {
        "description": "Key factors affecting software application performance",
        "keywords": {
            "Algorithm Efficiency": "Complexity and optimization of code logic.",
            "Hardware Resources": "CPU speed, memory capacity, and storage performance.",
            "Network Latency & Bandwidth": "Especially for distributed or cloud-based apps.",
            "Concurrency & Load Handling": "Threading, async processing, and scaling ability.",
            "Database Query Optimization": "Indexing, caching, and reducing I/O bottlenecks."
        }
    },
    "Road Traffic": {
        "description": "Elements that affect road traffic flow and conditions",
        "keywords": {
            "Road Infrastructure": "Quality, layout, and capacity of roads.",
            "Traffic Volume": "Number of vehicles and peak-hour surges.",
            "Traffic Signals & Control": "Synchronization, signage, and smart systems.",
            "Accidents & Roadworks": "Unexpected disruptions reducing flow.",
            "Weather Conditions": "Rain, snow, and fog affecting speed and safety."
        }
    }
}

def get_all_topics():
    """Return list of all topic names."""
    return list(TOPICS.keys())

def get_topic_data(topic_name):
    """Return data for a specific topic."""
    return TOPICS.get(topic_name)

def get_keywords_list(topic_name):
    """Return list of keywords for a specific topic."""
    topic_data = TOPICS.get(topic_name)
    if topic_data:
        return list(topic_data["keywords"].keys())
    return []


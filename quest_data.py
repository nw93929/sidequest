import random
import pandas as pd
from datetime import datetime, timedelta


# shared quest data so we don't copy paste the same thing on every page
def build_quests():
    random.seed(42)
    categories = ["🎲 Games", "🏐 Sports", "🍕 Food & Drink", "🎤 Music", "🥾 Outdoors", "📚 Study"]
    locations = [
        ("The Haven Brewery", 0.5), ("McIntire Park", 1.2), ("Downtown Mall", 0.8),
        ("Rivanna Trail", 2.4), ("Corner Cafe", 0.3), ("UVA Lawn", 1.0),
        ("IX Art Park", 1.5), ("Random Row Brewing", 0.7), ("Dairy Market", 0.9),
        ("Pen Park", 3.1), ("Carter Mountain", 4.8), ("Kardinal Hall", 1.8),
    ]
    titles = [
        "Casual Board Games", "Pickup Volleyball", "Trivia Night",
        "Karaoke Night", "Sunset Hike", "Study Session",
        "Pickup Basketball", "Open Mic Night", "Taco Tuesday Hangout",
        "Frisbee at the Park", "Coffee & Sketch", "Yoga in the Park",
        "D&D One-Shot", "Rock Climbing Meetup", "Poetry Reading",
    ]
    hosts = [
        "Jamie R.", "Alex T.", "Morgan K.", "Sam W.", "Riley P.",
        "Jordan B.", "Casey M.", "Quinn L.", "Dakota F.", "Avery S.",
    ]
    now = datetime.now()
    quests = []
    for i, title in enumerate(titles):
        loc_name, dist = random.choice(locations)
        cat = random.choice(categories)
        hour_offset = random.choice([0.5, 1, 1.5, 2, 3, 4])
        start = now + timedelta(hours=hour_offset)
        spots_total = random.randint(4, 12)
        spots_taken = random.randint(1, spots_total - 1)
        quests.append({
            "id": i,
            "title": title,
            "category": cat,
            "location": loc_name,
            "distance_mi": dist,
            "start_time": start.strftime("%I:%M %p"),
            "start_dt": start,
            "host": random.choice(hosts),
            "spots_total": spots_total,
            "spots_taken": spots_taken,
            "spots_left": spots_total - spots_taken,
            "description": f"Come hang out! {title} at {loc_name}. All are welcome.",
        })
    return quests


def get_quest_df():
    return pd.DataFrame(build_quests())


def get_quest_dict():
    quests = build_quests()
    return {q["id"]: q for q in quests}

"""Seeds iniciales: categorias y challenges. Se ejecutan al arrancar si las
tablas estan vacias. Solo prototipo — en produccion se gestionarian via Alembic.
"""

from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.challenge import Challenge

INITIAL_CATEGORIES = [
    {"name": "Food", "icon": "restaurant", "description": "Meals, groceries and snacks"},
    {"name": "Transport", "icon": "directions_bus", "description": "Bus, metro, gas and rides"},
    {"name": "Entertainment", "icon": "movie", "description": "Movies, games and outings"},
    {"name": "Health", "icon": "local_hospital", "description": "Medical, pharmacy and wellness"},
    {"name": "Education", "icon": "school", "description": "Books, courses and supplies"},
    {"name": "Other", "icon": "more_horiz", "description": "Miscellaneous expenses"},
]


INITIAL_CHALLENGES = [
    {
        "kind": "quiz",
        "title": "Money Basics",
        "xp_reward": 30,
        "content": {
            "questions": [
                {
                    "question": "If you save $10 every week for a year, how much will you have saved?",
                    "options": ["$120", "$520", "$480", "$1,040"],
                    "correct": 1,
                    "explanation": "$10 x 52 weeks = $520. Small consistent savings add up.",
                },
                {
                    "question": "Which of these is a 'need' rather than a 'want'?",
                    "options": ["New sneakers", "Movie tickets", "School supplies", "Video game"],
                    "correct": 2,
                    "explanation": "School supplies are essential for education; the others are wants.",
                },
                {
                    "question": "What does a budget help you do?",
                    "options": [
                        "Spend more money",
                        "Track and control your spending",
                        "Avoid saving money",
                        "Ignore your expenses",
                    ],
                    "correct": 1,
                    "explanation": "A budget helps you understand where your money goes.",
                },
            ],
        },
    },
    {
        "kind": "simulation",
        "title": "Smart Spending",
        "xp_reward": 25,
        "content": {
            "scenario": "You received $200 from your part-time job. You need to cover essentials AND save for your headphone goal.",
            "budget": 200,
            "categories_label": "Rent + Food",
            "choices": [
                {
                    "label": "Spend it all, enjoy now",
                    "split": "$120 fun - $80 food - $0 savings",
                    "tag": "Risky",
                    "outcome": "Great weekend, but you're broke until next paycheck. Goal delayed a month.",
                    "savings": 0,
                    "xp": 5,
                },
                {
                    "label": "Balance spending and saving",
                    "split": "$50 fun - $80 food - $70 savings",
                    "tag": "Smart",
                    "outcome": "You covered needs, had fun AND saved $70. Goal in ~2 months at this pace.",
                    "savings": 70,
                    "xp": 25,
                },
                {
                    "label": "Save everything, skip fun",
                    "split": "$0 fun - $80 food - $120 savings",
                    "tag": "Not ideal",
                    "outcome": "Faster goal, but skipping fun isn't sustainable. Balance builds habits.",
                    "savings": 120,
                    "xp": 15,
                },
            ],
        },
    },
]


def seed_categories(db: Session) -> None:
    if db.query(Category).count() > 0:
        return
    for cat_data in INITIAL_CATEGORIES:
        db.add(Category(**cat_data))
    db.commit()


def seed_challenges(db: Session) -> None:
    if db.query(Challenge).count() > 0:
        return
    for ch_data in INITIAL_CHALLENGES:
        db.add(Challenge(**ch_data))
    db.commit()

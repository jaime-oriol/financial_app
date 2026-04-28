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
        "level": 1,
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
        "level": 1,
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
    {
        "kind": "quiz",
        "title": "Smart Saver",
        "xp_reward": 30,
        "level": 2,
        "content": {
            "questions": [
                {
                    "question": "What's the recommended share of income to save each month?",
                    "options": ["At least 5%", "At least 10-20%", "At least 50%", "Whatever is left"],
                    "correct": 1,
                    "explanation": "10-20% is the rule of thumb. Saving 'whatever is left' rarely works.",
                },
                {
                    "question": "An emergency fund should ideally cover...",
                    "options": [
                        "1 weekend of fun",
                        "3-6 months of essential expenses",
                        "A new phone",
                        "Nothing — credit cards exist",
                    ],
                    "correct": 1,
                    "explanation": "3-6 months of essentials is the standard target so a setback doesn't break you.",
                },
                {
                    "question": "Why is paying yourself first a good habit?",
                    "options": [
                        "It feels good",
                        "Saving becomes automatic, not the leftover",
                        "It hides money from your bank",
                        "It avoids taxes",
                    ],
                    "correct": 1,
                    "explanation": "Automating savings before spending makes the habit stick.",
                },
            ],
        },
    },
    {
        "kind": "simulation",
        "title": "Friday Night",
        "xp_reward": 25,
        "level": 1,
        "content": {
            "scenario": "It's Friday and you have $50 cash. Friends invite you to a concert ($35) and you also need to save for your laptop goal.",
            "budget": 50,
            "categories_label": "Fun + Save",
            "choices": [
                {
                    "label": "Concert + dinner out",
                    "split": "$35 concert - $15 food - $0 savings",
                    "tag": "Risky",
                    "outcome": "Awesome night! Zero saved this week. The laptop just got further away.",
                    "savings": 0,
                    "xp": 5,
                },
                {
                    "label": "Cheaper plan: home pre-game + concert",
                    "split": "$35 concert - $5 snacks - $10 savings",
                    "tag": "Smart",
                    "outcome": "Same fun, $10 closer to your laptop. This is the move every weekend.",
                    "savings": 10,
                    "xp": 25,
                },
                {
                    "label": "Skip the concert, save it all",
                    "split": "$0 fun - $5 snacks - $45 savings",
                    "tag": "Not ideal",
                    "outcome": "Big jump for the laptop, but missing every plan kills motivation.",
                    "savings": 45,
                    "xp": 15,
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Needs vs Wants",
        "xp_reward": 30,
        "level": 1,
        "content": {
            "questions": [
                {
                    "question": "Which is a NEED, not a want?",
                    "options": ["Designer sneakers", "Daily bus pass to school", "Streaming subscription", "Newest phone"],
                    "correct": 1,
                    "explanation": "Transport to school is essential. Subscriptions and brands are wants.",
                },
                {
                    "question": "A friend says 'I need a new gaming console'. Most accurate?",
                    "options": [
                        "It's a need if his old one broke",
                        "It's a want — entertainment is non-essential",
                        "It's a need if his friends have it",
                        "All consoles are needs",
                    ],
                    "correct": 1,
                    "explanation": "Entertainment is a want. Replacing a broken one doesn't change that.",
                },
                {
                    "question": "Best test to spot a want disguised as a need?",
                    "options": [
                        "Ask: would I survive without it for 3 months?",
                        "Check the price",
                        "Ask my friends",
                        "See if it's on sale",
                    ],
                    "correct": 0,
                    "explanation": "If life keeps working without it for months, it's a want.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Emergency Fund 101",
        "xp_reward": 30,
        "level": 2,
        "content": {
            "questions": [
                {
                    "question": "Best place to keep your emergency fund?",
                    "options": ["Stocks", "A savings account you can access fast", "Crypto", "In cash at home"],
                    "correct": 1,
                    "explanation": "Liquidity matters. You need it instantly when an emergency hits.",
                },
                {
                    "question": "Which counts as a real emergency?",
                    "options": ["A flash sale", "Car broke down", "Concert tickets dropped", "New game release"],
                    "correct": 1,
                    "explanation": "Unexpected and necessary expenses are emergencies. Sales are not.",
                },
                {
                    "question": "After using your emergency fund, the priority is:",
                    "options": ["Forget about it", "Rebuild it as soon as you can", "Move it to crypto", "Borrow more"],
                    "correct": 1,
                    "explanation": "An empty emergency fund leaves you exposed. Refill it ASAP.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Compound Interest",
        "xp_reward": 30,
        "level": 3,
        "content": {
            "questions": [
                {
                    "question": "Compound interest means...",
                    "options": [
                        "Interest only on the original deposit",
                        "Interest on your interest too",
                        "A bank fee",
                        "Tax on savings",
                    ],
                    "correct": 1,
                    "explanation": "You earn interest on your interest. That's why time matters so much.",
                },
                {
                    "question": "$1,000 at 7% per year for 10 years (compounded) becomes ~?",
                    "options": ["$1,070", "$1,700", "$1,967", "$10,000"],
                    "correct": 2,
                    "explanation": "1000 x 1.07^10 ≈ $1,967. Almost double in 10 years.",
                },
                {
                    "question": "Starting earlier with a small amount usually beats...",
                    "options": [
                        "Starting later with a bigger amount",
                        "Never starting",
                        "Saving in cash",
                        "Both A and B",
                    ],
                    "correct": 3,
                    "explanation": "Time is the key ingredient — start early, even small.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Credit Cards 101",
        "xp_reward": 30,
        "level": 3,
        "content": {
            "questions": [
                {
                    "question": "Best practice with a credit card?",
                    "options": [
                        "Pay only the minimum",
                        "Pay the full balance every month",
                        "Skip payments if you can",
                        "Max it out for rewards",
                    ],
                    "correct": 1,
                    "explanation": "Paying in full avoids interest, which is the real cost of credit.",
                },
                {
                    "question": "What does APR mean?",
                    "options": [
                        "Annual Premium Rate",
                        "Annual Percentage Rate (yearly cost of borrowing)",
                        "Approved Purchase Refund",
                        "Average Payment Required",
                    ],
                    "correct": 1,
                    "explanation": "APR = the yearly cost of borrowing money on the card.",
                },
                {
                    "question": "If APR is 20% and you carry $500 unpaid for a year...",
                    "options": ["You owe $500", "You owe ~$600", "You owe $510", "You owe nothing extra"],
                    "correct": 1,
                    "explanation": "20% on $500 = $100 extra. That's the cost of not paying in full.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Spotting Scams",
        "xp_reward": 30,
        "level": 2,
        "content": {
            "questions": [
                {
                    "question": "DM offers 'guaranteed 50% returns in a week'. Most likely it is...",
                    "options": ["A great deal", "A scam", "A bank promo", "Government aid"],
                    "correct": 1,
                    "explanation": "If it sounds too good to be true, it almost always is.",
                },
                {
                    "question": "A 'bank' emails asking for your password. You should...",
                    "options": [
                        "Reply with the password",
                        "Click the link to verify",
                        "Ignore and contact the bank directly",
                        "Forward it to friends",
                    ],
                    "correct": 2,
                    "explanation": "Real banks never ask for passwords. Always go via the official channel.",
                },
                {
                    "question": "Strongest defense against scams?",
                    "options": [
                        "Antivirus only",
                        "Slow down before paying or sharing data",
                        "Trust senders you know",
                        "Pay with a debit card",
                    ],
                    "correct": 1,
                    "explanation": "Urgency is the scammer's weapon. Pause, verify, then act.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Investing for Beginners",
        "xp_reward": 30,
        "level": 3,
        "content": {
            "questions": [
                {
                    "question": "An index fund is...",
                    "options": [
                        "A single hot stock",
                        "A basket of many stocks tracking a market",
                        "A type of crypto",
                        "A savings account",
                    ],
                    "correct": 1,
                    "explanation": "Index funds spread risk across many companies. Boring but effective.",
                },
                {
                    "question": "Diversification means...",
                    "options": [
                        "Putting everything in one stock",
                        "Spreading money across different assets",
                        "Buying only crypto",
                        "Avoiding stocks entirely",
                    ],
                    "correct": 1,
                    "explanation": "Don't put all eggs in one basket. Spread risk.",
                },
                {
                    "question": "For long-term goals, historically the best return came from...",
                    "options": ["Cash under the mattress", "Diversified stocks held many years", "Lottery tickets", "Crypto only"],
                    "correct": 1,
                    "explanation": "Time + diversification = the boring winning combo.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Smart Shopping",
        "xp_reward": 30,
        "level": 2,
        "content": {
            "questions": [
                {
                    "question": "'Buy one get one free' on something you didn't need is...",
                    "options": [
                        "A win — free stuff!",
                        "Spending you didn't plan",
                        "Always a great deal",
                        "Required by law",
                    ],
                    "correct": 1,
                    "explanation": "If you didn't need it, it's not a saving — it's spending.",
                },
                {
                    "question": "Best moment to make a big purchase?",
                    "options": [
                        "Right when you see the ad",
                        "After waiting 24h to confirm you still want it",
                        "After scrolling for 5 hours",
                        "Whenever a friend pushes you",
                    ],
                    "correct": 1,
                    "explanation": "The 24h rule kills most impulse buys.",
                },
                {
                    "question": "Compare 'price per unit' helps you...",
                    "options": [
                        "Look smarter at the store",
                        "Spot which size/brand is actually cheaper",
                        "Get rewards points",
                        "Avoid taxes",
                    ],
                    "correct": 1,
                    "explanation": "Bigger isn't always cheaper — price per unit reveals the truth.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Debt vs Savings",
        "xp_reward": 30,
        "level": 3,
        "content": {
            "questions": [
                {
                    "question": "If you owe money at 20% APR but a savings account pays 2%, you should...",
                    "options": [
                        "Save first, ignore the debt",
                        "Pay down the debt first",
                        "Take more debt",
                        "Move to crypto",
                    ],
                    "correct": 1,
                    "explanation": "20% > 2%. Paying high-interest debt is the highest-return move.",
                },
                {
                    "question": "Good debt vs bad debt — which is closer to good?",
                    "options": [
                        "Buying clothes on credit",
                        "Loan for education or productive asset",
                        "Borrowing for a vacation",
                        "All debt is good",
                    ],
                    "correct": 1,
                    "explanation": "Debt that increases your earning power can be worth it; consumption debt rarely is.",
                },
                {
                    "question": "Minimum payments on a credit card mostly cover...",
                    "options": [
                        "The principal",
                        "Mostly interest, principal barely moves",
                        "Nothing",
                        "Future purchases",
                    ],
                    "correct": 1,
                    "explanation": "That's why minimum payments stretch debt for years.",
                },
            ],
        },
    },
    {
        "kind": "quiz",
        "title": "Subscriptions Trap",
        "xp_reward": 30,
        "level": 2,
        "content": {
            "questions": [
                {
                    "question": "5 subscriptions at $10/month cost you per year...",
                    "options": ["$50", "$120", "$600", "$1,200"],
                    "correct": 2,
                    "explanation": "5 x 10 x 12 = $600. Subscriptions add up fast.",
                },
                {
                    "question": "Best habit with subscriptions?",
                    "options": [
                        "Subscribe and forget",
                        "Review every 3 months and cancel unused",
                        "Subscribe to everything friends mention",
                        "Pay yearly to save",
                    ],
                    "correct": 1,
                    "explanation": "Out-of-sight, out-of-mind subscriptions silently drain your money.",
                },
                {
                    "question": "Free trials usually become charges if you...",
                    "options": ["Use the product a lot", "Don't cancel before the deadline", "Watch ads", "Refer a friend"],
                    "correct": 1,
                    "explanation": "Set a calendar reminder the day you start any free trial.",
                },
            ],
        },
    },
    {
        "kind": "simulation",
        "title": "Birthday Cash",
        "xp_reward": 25,
        "level": 1,
        "content": {
            "scenario": "Your relatives gave you $100 for your birthday. You have a savings goal but also haven't treated yourself in a while.",
            "budget": 100,
            "categories_label": "Treat + Save",
            "choices": [
                {
                    "label": "Spend all on a new gadget",
                    "split": "$100 gadget - $0 savings",
                    "tag": "Risky",
                    "outcome": "New shiny thing today, zero progress on your goal. Familiar feeling.",
                    "savings": 0,
                    "xp": 5,
                },
                {
                    "label": "Split: small treat + save the rest",
                    "split": "$25 treat - $75 savings",
                    "tag": "Smart",
                    "outcome": "Enjoyed the day AND your goal jumped $75. This is what financial maturity looks like.",
                    "savings": 75,
                    "xp": 25,
                },
                {
                    "label": "Save it all, no treat",
                    "split": "$0 treat - $100 savings",
                    "tag": "Not ideal",
                    "outcome": "Big save, but birthdays are once a year. Some celebration is healthy.",
                    "savings": 100,
                    "xp": 15,
                },
            ],
        },
    },
    {
        "kind": "simulation",
        "title": "First Paycheck",
        "xp_reward": 25,
        "level": 2,
        "content": {
            "scenario": "Your first summer job paid $500. You've been waiting for this. Rent goes to your parents ($150) and the rest is up to you.",
            "budget": 500,
            "categories_label": "Rent + You",
            "choices": [
                {
                    "label": "Spend most on yourself",
                    "split": "$150 rent - $300 fun - $50 savings",
                    "tag": "Risky",
                    "outcome": "Big weekend, but you barely saved your first 'real' paycheck. Habit-setting moment lost.",
                    "savings": 50,
                    "xp": 5,
                },
                {
                    "label": "50/30/20 split (needs/wants/save)",
                    "split": "$150 rent - $200 wants - $150 savings",
                    "tag": "Smart",
                    "outcome": "Classic 50/30/20 split. Habit set. Your future self thanks you.",
                    "savings": 150,
                    "xp": 25,
                },
                {
                    "label": "Save almost everything",
                    "split": "$150 rent - $50 wants - $300 savings",
                    "tag": "Not ideal",
                    "outcome": "Huge save, but extreme saving without enjoyment usually breaks within a few months.",
                    "savings": 300,
                    "xp": 15,
                },
            ],
        },
    },
    {
        "kind": "simulation",
        "title": "Phone Upgrade",
        "xp_reward": 25,
        "level": 2,
        "content": {
            "scenario": "Your phone still works but a friend just got the new model. Tempting. You've saved $400 toward a trip.",
            "budget": 400,
            "categories_label": "Want + Goal",
            "choices": [
                {
                    "label": "Buy the new phone now",
                    "split": "$400 phone - $0 savings",
                    "tag": "Risky",
                    "outcome": "Shiny phone today. Your trip goal: gone. Repeat this pattern and goals never happen.",
                    "savings": 0,
                    "xp": 5,
                },
                {
                    "label": "Keep your phone, keep saving",
                    "split": "$0 phone - $400 savings",
                    "tag": "Smart",
                    "outcome": "Your phone still does the job. Trip goal intact and growing.",
                    "savings": 400,
                    "xp": 25,
                },
                {
                    "label": "Sell old phone, buy refurbished",
                    "split": "$200 net upgrade - $200 savings",
                    "tag": "Not ideal",
                    "outcome": "Compromise. Better than full new, worse than skipping. Decent middle ground.",
                    "savings": 200,
                    "xp": 15,
                },
            ],
        },
    },
]


def seed_categories(db: Session) -> None:
    """Insertar categorias por nombre. Idempotente: anade solo las que falten."""
    existing = {c.name for c in db.query(Category).all()}
    new = [c for c in INITIAL_CATEGORIES if c["name"] not in existing]
    for cat_data in new:
        db.add(Category(**cat_data))
    if new:
        db.commit()


def seed_challenges(db: Session) -> None:
    """Insertar challenges por titulo y sincronizar nivel/xp si cambia en el seed.
    Idempotente: no toca los attempts del usuario, solo metadata del challenge.
    """
    existing = {c.title: c for c in db.query(Challenge).all()}
    changed = False
    for ch_data in INITIAL_CHALLENGES:
        title = ch_data["title"]
        if title in existing:
            current = existing[title]
            new_level = ch_data.get("level", 1)
            if current.level != new_level:
                current.level = new_level
                changed = True
        else:
            db.add(Challenge(**ch_data))
            changed = True
    if changed:
        db.commit()

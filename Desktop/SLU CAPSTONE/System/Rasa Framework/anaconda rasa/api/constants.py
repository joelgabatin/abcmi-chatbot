"""
api/constants.py
Shared constants: fallback responses, intent keywords, state-reset keywords.
"""

# Fallback responses used when the database is unreachable
FALLBACK_RESPONSES = {
    "utter_greet": "Welcome to Grace Church! I'm here to help. How are you doing today?",
    "utter_mission": "Our mission is to glorify God by making disciples of all nations.",
    "utter_vision": "Our vision is to be a Christ-centered community transforming lives through the Gospel.",
    "utter_history": "ABCMI Church has a rich history of serving the community. Please contact us for more details.",
    "utter_statement_of_belief": "We believe in the authority of Scripture, the Trinity, salvation through Jesus Christ, and the resurrection.",
    "utter_driving_force": "The driving force of our church is rooted in faith and service. Please contact us for more details.",
    "utter_core_values": "Our core values guide everything we do. Please contact us for more details.",
    "utter_branches": "I can help you find a church branch near you. Please try again later.",
    "utter_total_branches": "I couldn't retrieve the total branch count right now. Please try again.",
    "utter_local_branches": "I couldn't retrieve local branch information right now. Please try again.",
    "utter_international_branches": "I couldn't retrieve international branch information right now. Please try again.",
    "utter_pastors": "I couldn't retrieve the list of pastors right now. Please try again.",
    "utter_goodbye": "God bless you! Feel free to return if you have more questions. Goodbye!",
}

# Intent keyword map — order matters: more specific intents must come before general ones.
# classify_intent() iterates this dict in insertion order and returns on first match.
INTENT_KEYWORDS = {
    # Branch count / list queries (must be before ask_branches so they match first)
    "ask_local_branches": [
        "how many local", "local branches", "list local branch",
        "what are the local branch", "local church branch", "philippines branch",
    ],
    "ask_international_branches": [
        "how many international", "international branches", "international branch",
        "list international", "what are the international branch",
    ],
    "ask_total_branches": [
        "how many branches", "total branches", "number of branches",
        "how many church branches", "count of branches", "how many abcmi branch",
    ],

    # Branch finder (multi-turn conversation)
    "ask_branches": [
        "branch", "branches", "locate", "near me", "find a church", "find church",
        "church near", "what are your branches", "where are you located",
        "where can i find", "church location",
    ],

    # Church information
    "ask_mission": ["mission", "stand for", "aim", "accomplish", "goal"],
    "ask_vision": ["vision", "future", "dream", "becoming"],
    "ask_history": [
        "history", "founded", "started", "background", "milestone",
        "years", "how old", "who founded", "began", "abcmi",
    ],
    "ask_statement_of_belief": [
        "believe", "belief", "beliefs", "doctrine", "faith statement",
        "articles of faith", "what do you stand for spiritually",
    ],
    "ask_driving_force": [
        "driving force", "what drives", "motivates the church",
        "driving the church", "what propels",
    ],
    "ask_core_values": [
        "core values", "core value", "values of the church", "church values",
        "what are your values", "what values",
    ],

    # Pastor queries (must be before ask_branches to avoid "branch" keyword collision)
    "ask_pastors": [
        "who are the pastors", "list all pastors", "name the pastors",
        "all pastors", "pastors of abcmi", "church pastors", "who are your pastors",
        "who leads the church", "church leaders", "list of pastors",
        "pastors and their branches",
    ],
    # ask_specific_pastor is handled via regex in classifier.py — keywords here are a fallback
    "ask_specific_pastor": [
        "is your pastor", "a pastor named", "your pastor named",
        "one of your pastors", "is he a pastor", "is she a pastor",
    ],
    "ask_pastor_branch_schedule": [
        "service schedule", "branch schedule", "when is service",
        "what time is service", "when are the services", "worship schedule",
        "when does service start", "what time does service", "schedule of the branch",
        "church service schedule",
    ],

    # General
    "goodbye": ["bye", "goodbye", "see you", "farewell", "exit", "quit"],
    "greet": ["hello", "hi", "hey", "greet", "start", "begin"],
}

# If the user types any of these while mid-conversation, the state resets
STATE_RESET_KEYWORDS = [
    "mission", "vision", "history", "believe", "belief", "doctrine",
    "driving force", "core values", "cancel", "nevermind", "never mind",
    "stop", "reset", "start over",
]

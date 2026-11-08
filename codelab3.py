
import json
import streamlit as st


# JSON RULES
rules_json = '''
[
    {
        "name": "Top merit candidate",
        "priority": 100,
        "conditions": [
            ["cgpa", ">=", 3.7],
            ["co_curricular_score", ">=", 80],
            ["family_income", "<=", 8000],
            ["disciplinary_actions", "==", 0]
        ],
        "action": {
            "decision": "AWARD_FULL",
            "reason": "Excellent academic & co-curricular performance, with acceptable need"
        }
    },
    {
        "name": "Good candidate - partial scholarship",
        "priority": 80,
        "conditions": [
            ["cgpa", ">=", 3.3],
            ["co_curricular_score", ">=", 60],
            ["family_income", "<=", 12000],
            ["disciplinary_actions", "<=", 1]
        ],
        "action": {
        "decision": "AWARD_PARTIAL",
        "reason": "Good academic & involvement record with moderate need"
        }
    },
    {
        "name": "Need-based review",
        "priority": 70,
        "conditions": [
            ["cgpa", ">=", 2.5],
            ["family_income", "<=", 4000]
        ],
        "action": {
        "decision": "REVIEW",
        "reason": "High need but borderline academic score"
        }
    },
    {
        "name": "Low CGPA – not eligible",
        "priority": 95,
        "conditions": [
            ["cgpa", "<", 2.5]
        ],
        "action": {
        "decision": "REJECT",
        "reason": "CGPA below minimum scholarship requirement"
        }
    },
    {
        "name": "Serious disciplinary record",
        "priority": 90,
        "conditions": [
            ["disciplinary_actions", ">=", 2]
        ],
        "action": {
        "decision": "REJECT",
        "reason": "Too many disciplinary records"
        }
    }
]
'''

rules = json.loads(rules_json)


# CHECK CONDITIONS
def check_condition(applicant, condition):

    attribute, operator, value = condition
    actual_value = applicant[attribute]

    if operator == ">=":
        return actual_value >= value
    elif operator == "<=":
        return actual_value <= value
    elif operator == "==":
        return actual_value == value
    elif operator == "<":
        return actual_value < value
    elif operator == ">":
        return actual_value > value

    return False


# EVALUATE RULES
def evaluate_rules(applicant, rules):

    sorted_rules = sorted(
        rules,
        key=lambda rule: rule["priority"],
        reverse=True
    )

    for rule in sorted_rules:

        if all(
            check_condition(applicant, condition)
            for condition in rule["conditions"]
        ):

            return rule["name"], rule["action"]

    return "No matching rule", {
        "decision": "NO_DECISION",
        "reason": "No scholarship rule matched"
    }


# STREAMLIT INTERFACE
st.title("Scholarship Advisory System")

st.write("Enter applicant information below.")

st.subheader("Applicant Information")

cgpa = st.number_input(
    "CGPA",
    min_value=0.0,
    max_value=4.0,
    value=3.50
)

co_curricular_score = st.number_input(
    "Co-curricular Score",
    min_value=0,
    max_value=100,
    value=70
)

family_income = st.number_input(
    "Family Income (RM)",
    min_value=0,
    value=3000
)

disciplinary_actions = st.number_input(
    "Disciplinary Actions",
    min_value=0,
    value=0
)


# SCHOLARSHIP EVALUATION
if st.button("Evaluate Scholarship"):

    applicant = {
        "cgpa": cgpa,
        "co_curricular_score": co_curricular_score,
        "family_income": family_income,
        "disciplinary_actions": disciplinary_actions
    }

    rule_name, action = evaluate_rules(applicant, rules)

    st.subheader("Scholarship Decision")

    st.write("Matched Rule:", rule_name)

    st.write("Decision:", action["decision"])

    st.write("Reason:", action["reason"])

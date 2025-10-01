import re

# A single, robust regex to capture all parts of a question at once.
# re.S (or re.DOTALL) makes '.' match newlines, handling multi-line questions.
QUESTION_PATTERN= re.compile( r"\*\*Question \d+\*\*\s*(.*?)\s*A\)\s*(.*?)\s*B\)\s*(.*?)\s*C\)\s*(.*?)\s*D\)\s*(.*?)\s*\*\*Answer: [A-D]\)\s*(.*?)\*\*", re.S )

ERROR_MESSAGES={
    "incomplete_fields":"Please fill in all fields. Provide either a Class or a Job Field.",
    "api_failed":"API request failed.",
    "parse_failed": "Could not parse AI response.",
}
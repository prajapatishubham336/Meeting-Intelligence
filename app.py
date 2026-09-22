from pathlib import Path
from typing import List, Dict
import re
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


# APP CONFIGURATION
BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="MeetingMind AI")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# REQUEST MODEL
class TranscriptRequest(BaseModel):
    transcript: str


# TEXT UTILITIES
def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,:;-")

def split_sentences(transcript: str) -> List[str]:
    """
    Supports:
    Rahul: Backend will be completed by Wednesday.
    Priya: Testing will start after backend approval.
    """
    transcript = transcript.replace("\r\n", "\n").replace("\r", "\n")
    lines = []

    for line in transcript.split("\n"):
        line = line.strip()
        if not line:
            continue
        # Keep speaker-based lines together
        if re.match(r"^[A-Za-z][A-Za-z .'-]{1,35}:\s*", line):
            lines.append(line)
        else:
            parts = re.split(r"(?<=[.!?])\s+", line)
            lines.extend([p.strip() for p in parts if p.strip()])
    return lines

def extract_speaker_and_text(sentence: str):
    match = re.match(
        r"^\s*([A-Za-z][A-Za-z .'-]{1,35})\s*:\s*(.+)$",
        sentence
    )

    if match:
        speaker = clean_text(match.group(1))
        text = clean_text(match.group(2))
        return speaker, text
    return "Unassigned", clean_text(sentence)

def normalize_task(text: str) -> str:
    text = clean_text(text)
    # Remove speaker/pronouns
    text = re.sub(
        r"^(i|we|you|they|he|she)\s+"
        r"(will|shall|can|should|must)\s+",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove leading articles
    text = re.sub(
        r"^(the|a|an)\s+",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove deadline phrases
    text = re.sub(
        r"\s+(by|on)\s+"
        r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|"
        r"tomorrow|today|tonight|EOD|end of day).*$",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove dependency/action wording
    text = re.sub(
        r"\b(depends on|must be|needs to be|has to be|"
        r"should be|will be|is|are|was|were)\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove completion words
    text = re.sub(
        r"\b(completed|complete|finished|approved|ready|done|"
        r"successfully)\b",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(r"\s+", " ", text).strip(" .,;:-")
    if not text:
        return "Required task"
    return text.capitalize()

def extract_deadline(text: str):
    patterns = [
        r"\bby\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
        r"\bon\s+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
        r"\bby\s+(tomorrow|today|tonight|EOD|end of day)\b",
        r"\bon\s+(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+)\b",
        r"\bby\s+(\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+)\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)
    return "Not specified"


# DECISION EXTRACTION
def extract_decisions(items: List[Dict]) -> List[str]:
    decisions = []

    decision_patterns = [
        r"\bwe decided\b",
        r"\bdecision\b",
        r"\bagreed\b",
        r"\bapproved\b",
        r"\bwill launch\b",
        r"\bis scheduled\b",
        r"\bhas been approved\b",
        r"\bfinalized\b",
        r"\bconfirmed\b",
    ]

    for item in items:
        text = item["text"]
        if any(
            re.search(pattern, text, flags=re.IGNORECASE)
            for pattern in decision_patterns
        ):
            decisions.append(text)
    return list(dict.fromkeys(decisions))

# ACTION EXTRACTION
def extract_actions(items: List[Dict]) -> List[Dict]:
    actions = []

    action_patterns = [
        r"\bwill\b",
        r"\bshall\b",
        r"\bmust\b",
        r"\bneed to\b",
        r"\bneeds to\b",
        r"\bhas to\b",
        r"\bshould\b",
        r"\bresponsible for\b",
        r"\bcomplete\b",
        r"\bstart\b",
        r"\bprepare\b",
        r"\bdeploy\b",
        r"\btest\b",
        r"\bfinish\b",
    ]

    ignored_patterns = [
        r"\bbefore\b",
        r"\bafter\b",
        r"\bonce\b",
        r"\bdepends on\b",
        r"\bprerequisite\b",
    ]

    for item in items:
        text = item["text"]
        has_action = any(
            re.search(pattern, text, flags=re.IGNORECASE)
            for pattern in action_patterns)
        is_dependency_only = any(
            re.search(pattern, text, flags=re.IGNORECASE)
            for pattern in ignored_patterns)

        if has_action and not (
            is_dependency_only
            and not re.search(r"\bwill\b|\bmust\b|\bneed to\b", text, re.I)):
            actions.append({
                "task": text,
                "owner": item["speaker"],
                "deadline": extract_deadline(text),
                "status": "Pending"
            })

    return actions

# DEPENDENCY EXTRACTION
def add_dependency(
    dependencies: List[Dict],
    source: str,
    target: str,
    relation: str
):
    source = normalize_task(source)
    target = normalize_task(target)
    if source.lower() == target.lower():
        return
    dependency = {
        "from": source,
        "to": target,
        "type": relation
    }

    if dependency not in dependencies:
        dependencies.append(dependency)

def extract_dependencies(items):
    dependencies = []
    def clean_text(text):
        text = text.strip(" .,:;!?")
        text = re.sub(r"\s+", " ", text)

        # Remove starting articles
        text = re.sub(r"^(the|a|an)\s+", "", text, flags=re.I)

        # Remove first-person action phrases
        text = re.sub(
            r"^(i|we)\s+(will|shall|can|must|should)\s+",
            "",
            text,
            flags=re.I
        )

        # Remove action verbs from task names
        text = re.sub(
            r"^(begin|start|proceed with|initiate)\s+",
            "",
            text,
            flags=re.I
        )

        # Remove deadline phrases
        text = re.sub(
            r"\s+(by|on)\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
            r"(\s+evening|\s+morning|\s+afternoon)?$",
            "",
            text,
            flags=re.I
        )

        return text.strip(" .,:;!?").capitalize()
    for item in items:
        text = item.get("text", "")

        # Split lines containing multiple sentences
        sentences = re.split(r"(?<=[.!?])\s+", text)
        for sentence in sentences:
            sentence = sentence.strip()

            if not sentence:
                continue
            # Pattern 1:
            # Payment gateway integration depends on product catalog approval
            match = re.search(
                r"(.+?)\s+depends\s+on\s+(.+?)(?:[.!?]|$)",
                sentence,
                flags=re.I
            )

            if match:
                target = clean_text(match.group(1))
                source = clean_text(match.group(2))

                dependencies.append({
                    "from": source,
                    "to": target,
                    "type": "required before"
                })
                continue

            # Once payment gateway is ready, I will begin integration testing
            match = re.search(
                r"once\s+(.+?),\s*(?:i|we)\s+will\s+(.+?)(?:[.!?]|$)",
                sentence,
                flags=re.I
            )

            if match:
                source = clean_text(match.group(1))
                target = clean_text(match.group(2))

                dependencies.append({
                    "from": source,
                    "to": target,
                    "type": "required before"
                })
                continue

            # Checkout module must be tested before production release
            match = re.search(
                r"(.+?)\s+(?:must be|needs to be|should be)\s+tested\s+before\s+(.+?)(?:[.!?]|$)",
                sentence,
                flags=re.I
            )

            if match:
                source = clean_text(match.group(1) + " testing")
                target = clean_text(match.group(2))

                dependencies.append({
                    "from": source,
                    "to": target,
                    "type": "required before"
                })

    # Remove duplicate dependencies
    unique_dependencies = []
    seen = set()

    for dependency in dependencies:
        key = (
            dependency["from"].lower(),
            dependency["to"].lower(),
            dependency["type"].lower()
        )

        if key not in seen:
            seen.add(key)
            unique_dependencies.append(dependency)

    return unique_dependencies


# RISK EXTRACTION
def extract_risks(
    actions: List[Dict],
    dependencies: List[Dict]
) -> List[Dict]:
    risks = []

    for action in actions:
        if action["deadline"] == "Not specified":
            risks.append({
                "title": "Missing deadline",
                "detail": f"No deadline found for: {action['task']}",
                "level": "Medium"
            })

    if len(dependencies) >= 3:
        risks.append({
            "title": "Complex dependency chain",
            "detail": "Multiple task dependencies may create schedule delays.",
            "level": "High"
        })

    if not actions:
        risks.append({
            "title": "No action items",
            "detail": "No clear action items were identified in this transcript.",
            "level": "Low"
        })

    return risks

# MAIN ANALYSIS
def analyze_transcript(transcript: str) -> Dict:
    sentences = split_sentences(transcript)
    items = []
    for sentence in sentences:
        speaker, text = extract_speaker_and_text(sentence)

        if text:
            items.append({
                "speaker": speaker,
                "text": text
            })

    decisions = extract_decisions(items)
    actions = extract_actions(items)
    dependencies = extract_dependencies(items)
    risks = extract_risks(actions, dependencies)

    summary_text = (
        f"Analyzed {len(items)} sentences from the transcript — found "
        f"{len(decisions)} decision(s), {len(actions)} action item(s), "
        f"{len(dependencies)} dependency link(s), and {len(risks)} potential risk(s)."
    )

    return {
        "stats": {
            "decisions": len(decisions),
            "actions": len(actions),
            "dependencies": len(dependencies),
            "risks": len(risks)
        },
        "summary": summary_text,
        "decisions": decisions,
        "actions": actions,
        "dependencies": dependencies,
        "risks": risks
    }

# ROUTES
@app.get("/", response_class=HTMLResponse)
async def home():
    index_file = BASE_DIR / "templates" / "index.html"

    if not index_file.exists():
        return HTMLResponse(
            content="""
            <h1>MeetingMind AI</h1>
            <p>Error: templates/index.html file not found.</p>
            """,
            status_code=404
        )

    return FileResponse(
        path=str(index_file),
        media_type="text/html"
    )


@app.post("/analyze")
async def analyze(request: Request):
    try:
        data = await request.json()
        text = data.get("text", "").strip()
        if not text:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Please provide meeting transcript."
                }
            )

        result = analyze_transcript(text)
        return JSONResponse(content=result)

    except Exception as error:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Analysis failed: {str(error)}"
            }
        )

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "service": "MeetingMind AI"
    }
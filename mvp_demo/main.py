"""
Mirth AI Triage Copilot - Backend API
Run: uvicorn main:app --host 0.0.0.0 --port 8001 --reload
"""

import os
import json
import re
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import anthropic

app = FastAPI(title="Mirth AI Triage Copilot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load prompts
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"
HL7_PROMPT = (PROMPTS_DIR / "hl7_triage_prompt.txt").read_text()
MIRTH_PROMPT = (PROMPTS_DIR / "mirth_analyzer_prompt.txt").read_text()

# Claude client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


# ── Request / Response models ──────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    content: str
    input_type: str  # "hl7" | "mirth" | "batch"


class BatchRequest(BaseModel):
    messages: list[str]  # list of raw HL7 messages


# ── Helpers ────────────────────────────────────────────────────────────────

def call_claude(system_prompt: str, user_content: str) -> dict:
    """Call Claude API and parse JSON response."""
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}]
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if Claude wraps in ```json
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract JSON from response
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise HTTPException(status_code=500, detail=f"Claude returned non-JSON: {raw[:200]}")


def redact_phi(text: str) -> str:
    """Basic PHI redaction for demo safety."""
    # Redact common PID field patterns (names, DOBs, MRNs)
    # This is a demo-level redaction — not production HIPAA compliance
    redacted = re.sub(r'(?<=\|)[A-Z]+\^[A-Z]+(?:\^[A-Z]+)?(?=\|)', '[NAME REDACTED]', text)
    return redacted


# ── Endpoints ──────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/analyze/hl7")
def analyze_hl7(req: AnalyzeRequest):
    """
    Analyze a raw HL7 2.x message and return triage report.
    """
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="No HL7 content provided")

    if not req.content.strip().startswith("MSH"):
        raise HTTPException(status_code=400, detail="Content does not appear to be a valid HL7 message (must start with MSH)")

    try:
        result = call_claude(
            system_prompt=HL7_PROMPT,
            user_content=f"Analyze this HL7 message:\n\n{req.content}"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/mirth")
def analyze_mirth(req: AnalyzeRequest):
    """
    Analyze a Mirth Connect error log or channel export and return root cause + fix.
    """
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="No Mirth log content provided")

    try:
        result = call_claude(
            system_prompt=MIRTH_PROMPT,
            user_content=f"Analyze this Mirth Connect error log:\n\n{req.content}"
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/batch")
def analyze_batch(req: BatchRequest):
    """
    Analyze multiple HL7 messages and cluster failures by root cause pattern.
    """
    if not req.messages:
        raise HTTPException(status_code=400, detail="No messages provided")

    if len(req.messages) > 50:
        raise HTTPException(status_code=400, detail="Batch limit is 50 messages for demo")

    # Analyze each message
    results = []
    for i, msg in enumerate(req.messages):
        try:
            result = call_claude(
                system_prompt=HL7_PROMPT,
                user_content=f"Analyze this HL7 message:\n\n{msg}"
            )
            result["message_index"] = i
            results.append(result)
        except Exception as e:
            results.append({
                "message_index": i,
                "error": str(e),
                "severity_score": 0
            })

    # Cluster by dominant issue type
    clusters = {}
    for r in results:
        if "issues" in r and r["issues"]:
            key = r["issues"][0].get("type", "unknown")
            if key not in clusters:
                clusters[key] = {
                    "cluster_type": key,
                    "count": 0,
                    "severity_avg": 0,
                    "representative_issue": r["issues"][0],
                    "messages": []
                }
            clusters[key]["count"] += 1
            clusters[key]["severity_avg"] += r.get("severity_score", 0)
            clusters[key]["messages"].append(r.get("message_index"))

    # Calculate averages
    for c in clusters.values():
        if c["count"] > 0:
            c["severity_avg"] = round(c["severity_avg"] / c["count"], 1)

    # Sort clusters by count descending
    sorted_clusters = sorted(clusters.values(), key=lambda x: x["count"], reverse=True)

    return {
        "input_type": "batch",
        "total_messages": len(req.messages),
        "total_issues_found": sum(len(r.get("issues", [])) for r in results),
        "cluster_count": len(clusters),
        "clusters": sorted_clusters[:5],  # Top 5 clusters
        "individual_results": results,
        "summary": f"Analyzed {len(req.messages)} messages. Found {len(clusters)} distinct failure patterns. Top issue: {sorted_clusters[0]['cluster_type'] if sorted_clusters else 'none'}."
    }


# Serve frontend static files
web_dir = Path(__file__).parent.parent / "web"
if web_dir.exists():
    app.mount("/", StaticFiles(directory=str(web_dir), html=True), name="static")

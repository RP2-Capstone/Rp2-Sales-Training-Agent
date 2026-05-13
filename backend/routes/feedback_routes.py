from fastapi import APIRouter

router = APIRouter()

@router.get("/evaluate/{session_id}")       # ✅ session_id in URL
def evaluate(session_id: str, mode: str = "recent"):
    
    try:
        from database import get_conversation, save_feedback
        from feedback.evaluator import evaluate_conversation

        # ✅ Get limit based on mode
        if mode in ("full", "summary"):
            limit = 999        # all turns
        else:
            limit = 10         # last 10 only

        # ✅ Get THIS student's history
        history = get_conversation(
            session_id = session_id,
            limit      = limit
        )

        if not history:
            return {"error": "No conversation found for this session"}

        # ✅ Evaluate — result is already a dict
        result = evaluate_conversation(history, mode=mode)

        # ✅ Save feedback to database
        save_feedback(
            session_id = session_id,
            score      = result.get("final_score", 0),
            gemini_score  = result.get("gemini_score",  0),
            keyword_score = result.get("keyword_score", 0),
            tone_score    = result.get("tone_score",    0),
            summary    = str(result)
        )

        return {
            "session_id": session_id,
            "mode":       mode,
            "result":     result
        }

    except Exception as e:
        print("Evaluate Error:", e)
        return {"error": "Something went wrong during evaluation"}


@router.get("/history/{session_id}")        # ✅ session_id in URL
def feedback_history(session_id: str):
    """
    Get all past evaluations for one student

    Usage:
    GET /feedback/history/abc-123
    """
    try:
        from database import get_feedback_history

        history = get_feedback_history(session_id)

        if not history:
            return {"error": "No feedback history found"}

        return {
            "session_id": session_id,
            "history":    history
        }

    except Exception as e:
        print("History Error:", e)
        return {"error": "Something went wrong fetching history"}
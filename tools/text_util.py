from typing import Any

def extract_text(result: Any) -> str:
    if result is None:
        return ""
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        msgs = result.get("messages", []) or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "content", None) or getattr(last, "text", None) or str(last)
        for k in ("output", "text", "content", "result"):
            if k in result and isinstance(result[k], str):
                return result[k]
        return str(result)
    if hasattr(result, "messages"):
        msgs = getattr(result, "messages") or []
        if msgs:
            last = msgs[-1]
            return getattr(last, "content", None) or getattr(last, "text", None) or str(last)
    return str(result)
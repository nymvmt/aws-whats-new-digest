from fetcher import fetch_items
from comparator import load_history, save_history, extract_changes
from mailer import send_digest
from dotenv import load_dotenv
import json, time, os
from pathlib import Path
import urllib.request
load_dotenv()

def _debug_log(message: str, data: dict, *, run_id: str, hypothesis_id: str, location: str):
    payload = {
        "sessionId": "498edb",
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data,
        "timestamp": int(time.time() * 1000),
    }
    try:
        log_path = Path(__file__).resolve().parent / ".cursor" / "debug-498edb.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
        return
    except Exception:
        pass
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:7932/ingest/55503be4-f3d6-4928-8ef8-e75915b55859",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json", "X-Debug-Session-Id": "498edb"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=2).read()
    except Exception:
        pass

def main():
    run_id = os.getenv("DEBUG_RUN_ID", "local")
    _debug_log("digest start", {}, run_id=run_id, hypothesis_id="H0", location="digest.py:main:start")
    try:
        print("RSS 피드 수집 중...")
        current_items = fetch_items()

        print("이전 데이터 로드 중...")
        history = load_history()

        print("변경 사항 비교 중...")
        new_items, updated_items = extract_changes(current_items, history)
        print(f"신규: {len(new_items)}개 / 업데이트: {len(updated_items)}개")

        print("메일 발송 중...")
        send_digest(new_items, updated_items)

        print("히스토리 저장 중...")
        save_history(current_items)
        print("완료.")
        _debug_log(
            "digest done",
            {"current_items": len(current_items), "new_items": len(new_items), "updated_items": len(updated_items)},
            run_id=run_id,
            hypothesis_id="H0",
            location="digest.py:main:done",
        )
    except Exception as e:
        _debug_log("digest error", {"error": str(e)[:200]}, run_id=run_id, hypothesis_id="H0", location="digest.py:main:error")
        raise

if __name__ == "__main__":
    main()
from fetcher import fetch_items
from comparator import load_history, save_history, extract_changes
from mailer import send_digest
from dotenv import load_dotenv
load_dotenv()

def main():
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

if __name__ == "__main__":
    main()
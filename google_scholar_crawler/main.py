import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import signal
from types import FrameType
from typing import Iterator

DEFAULT_SCHOLAR_ID = "tWcg0ZsAAAAJ"


def normalize_author(author: dict, scholar_id: str) -> dict:
    """Validate a complete author response before replacing the last good snapshot."""
    if author.get("scholar_id") != scholar_id:
        raise ValueError("Scholar returned a different author ID")
    if not author.get("name"):
        raise ValueError("Scholar returned no author name")
    if type(author.get("citedby")) is not int or author["citedby"] < 0:
        raise ValueError("Scholar returned an invalid total citation count")
    publications = author.get("publications")
    if not isinstance(publications, list) or not publications:
        raise ValueError("Scholar returned no publication list; retaining prior data")

    indexed = {}
    for publication in publications:
        if not isinstance(publication, dict):
            raise ValueError("Scholar returned a malformed publication")
        publication_id = publication.get("author_pub_id", "")
        if not isinstance(publication_id, str) or not publication_id.startswith(
            f"{scholar_id}:"
        ):
            raise ValueError("Scholar returned a publication for an unexpected author")
        if publication_id in indexed:
            raise ValueError("Scholar returned duplicate publication IDs")
        count = publication.get("num_citations")
        if type(count) is not int or count < 0:
            raise ValueError("Scholar returned an invalid publication citation count")
        if not isinstance(publication.get("bib"), dict) or not publication["bib"].get(
            "title"
        ):
            raise ValueError("Scholar returned a publication without a title")
        indexed[publication_id] = publication

    snapshot = dict(author)
    snapshot["publications"] = indexed
    snapshot["updated"] = (
        datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    )
    return snapshot


def fetch_author(scholar_id: str) -> dict:
    from scholarly import scholarly

    scholarly.set_timeout(30)
    scholarly.set_retries(2)
    author = scholarly.search_author_id(scholar_id)
    scholarly.fill(author, sections=["basics", "indices", "counts", "publications"])
    return normalize_author(author, scholar_id)


def write_snapshot(snapshot: dict, output_dir: Path) -> None:
    """Write only fully validated, JSON-serializable responses."""
    shield = {
        "schemaVersion": 1,
        "label": "citations",
        "message": str(snapshot["citedby"]),
    }
    payloads = {
        "gs_data.json": json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        "gs_data_shieldsio.json": json.dumps(shield, ensure_ascii=False, indent=2)
        + "\n",
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, payload in payloads.items():
        destination = output_dir / filename
        pending = destination.with_suffix(".json.pending")
        pending.write_text(payload, encoding="utf-8")
        pending.replace(destination)


@contextmanager
def fetch_deadline(seconds: int) -> Iterator[None]:
    def expired(signum: int, frame: FrameType | None) -> None:
        # SystemExit cannot be swallowed by scholarly's broad retry handlers.
        raise SystemExit(
            "Google Scholar fetch exceeded its deadline; retaining prior data"
        )

    previous_handler = signal.signal(signal.SIGALRM, expired)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous_handler)


def update_snapshot(scholar_id: str, output_dir: Path, timeout_seconds: int) -> dict:
    with fetch_deadline(timeout_seconds):
        snapshot = fetch_author(scholar_id)
    write_snapshot(snapshot, output_dir)
    return snapshot


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Refresh Google Scholar citation data without overwriting failed fetches."
    )
    parser.add_argument(
        "--scholar-id",
        default=os.getenv("GOOGLE_SCHOLAR_ID", "").strip() or DEFAULT_SCHOLAR_ID,
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path(__file__).resolve().parent / "results"
    )
    parser.add_argument("--timeout-seconds", type=int, default=240)
    args = parser.parse_args()
    if args.timeout_seconds <= 0:
        parser.error("--timeout-seconds must be positive")
    snapshot = update_snapshot(args.scholar_id, args.output_dir, args.timeout_seconds)
    print(
        f"Updated {len(snapshot['publications'])} publications at {snapshot['updated']}."
    )


if __name__ == "__main__":
    main()

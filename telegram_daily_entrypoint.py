"""Run the existing Telegram lesson sender at most once per Madrid calendar day."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parent
DEFAULT_PROGRESS_PATH = ROOT / "progress" / "a1_daily.json"
MADRID_TZ = ZoneInfo("Europe/Madrid")


class EntrypointError(Exception):
    """Raised when publication state cannot be evaluated safely."""


def load_progress(path: Path) -> dict[str, object]:
    if not path.exists():
        return {"level": "a1", "last_published_lesson": 0, "history": []}
    return json.loads(path.read_text(encoding="utf-8"))


def last_successful_publication_date(progress: dict[str, object]) -> date | None:
    """Return the latest successful publication date in Europe/Madrid."""
    history = progress.get("history", [])
    if not isinstance(history, list):
        raise EntrypointError("Progress history must be a list.")

    timestamps: list[datetime] = []
    for entry in history:
        if not isinstance(entry, dict):
            continue
        published_at = entry.get("published_at_madrid")
        if not isinstance(published_at, str) or not published_at:
            continue
        try:
            timestamp = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise EntrypointError(f"Invalid published_at_madrid timestamp: {published_at!r}") from exc
        if timestamp.tzinfo is None:
            raise EntrypointError(
                f"published_at_madrid timestamp must include a timezone: {published_at!r}"
            )
        timestamps.append(timestamp.astimezone(MADRID_TZ))

    return max(timestamps).date() if timestamps else None


def should_publish_today(force: bool, now: datetime, progress: dict[str, object]) -> bool:
    if force:
        return True
    madrid_now = now.astimezone(MADRID_TZ)
    return last_successful_publication_date(progress) != madrid_now.date()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply the Madrid daily guard and run the lesson sender.")
    parser.add_argument("--level", default="a1")
    parser.add_argument("--progress-path", type=Path, default=DEFAULT_PROGRESS_PATH)
    parser.add_argument("--force", action="store_true", help="Bypass the Madrid daily publication guard.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    now = datetime.now(tz=MADRID_TZ)
    progress = load_progress(args.progress_path)
    last_date = last_successful_publication_date(progress)

    print(f"Madrid time: {now.isoformat()}")
    print(f"Last successful Madrid publication date: {last_date.isoformat() if last_date else 'none'}")

    if not should_publish_today(args.force, now, progress):
        print(f"Skipping: today's Madrid date ({now.date().isoformat()}) is already completed.")
        return 0

    if args.force:
        print("Force mode: bypassing the Madrid daily publication guard.")
    else:
        print(f"Publishing: no successful lesson exists for Madrid date {now.date().isoformat()}.")

    command = [
        sys.executable,
        str(ROOT / "telegram_daily_sender.py"),
        "--level",
        args.level.lower(),
        "--progress-path",
        str(args.progress_path),
        "--force",
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except EntrypointError as exc:
        print(f"telegram_daily_entrypoint error: {exc}", file=sys.stderr)
        raise SystemExit(1)

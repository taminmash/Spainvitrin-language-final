"""Run the existing Telegram lesson sender with a Madrid-calendar-day guard.

This wrapper tolerates delayed GitHub Actions starts while preserving the existing
sender, lesson ordering, direct TELEGRAM_CHAT_ID delivery, and progress updates.
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import date, datetime
from pathlib import Path

from telegram_daily_sender import (
    DEFAULT_LEVEL,
    DEFAULT_LESSONS_DIR,
    DEFAULT_PROGRESS_PATH,
    MADRID_TZ,
    SenderError,
    configure_stdio,
    load_progress,
    publish_next_lesson,
)


def last_successful_publication_date(progress: dict[str, object]) -> date | None:
    """Return the most recent successful publication date in Europe/Madrid."""
    history = progress.get("history", [])
    if not isinstance(history, list):
        raise SenderError("Progress history must be a list.")

    published_at_values: list[datetime] = []
    for entry in history:
        if not isinstance(entry, dict):
            continue
        published_at = entry.get("published_at_madrid")
        if not isinstance(published_at, str) or not published_at:
            continue
        try:
            timestamp = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise SenderError(f"Invalid published_at_madrid timestamp: {published_at!r}") from exc
        if timestamp.tzinfo is None:
            raise SenderError(
                f"published_at_madrid timestamp must include a timezone: {published_at!r}"
            )
        published_at_values.append(timestamp.astimezone(MADRID_TZ))

    return max(published_at_values).date() if published_at_values else None


def should_publish_today(force: bool, now: datetime, progress: dict[str, object]) -> bool:
    """Allow one successful publication per Madrid date unless explicitly forced."""
    if force:
        return True
    madrid_now = now.astimezone(MADRID_TZ)
    return last_successful_publication_date(progress) != madrid_now.date()


async def run_guarded(
    *,
    level: str,
    lessons_dir: Path,
    progress_path: Path,
    dry_run: bool,
    force: bool,
    keep_artifacts: bool,
) -> int:
    now = datetime.now(tz=MADRID_TZ)
    progress = load_progress(progress_path)
    last_date = last_successful_publication_date(progress)

    print(f"Madrid time: {now.isoformat()}")
    print(
        "Last successful Madrid publication date: "
        + (last_date.isoformat() if last_date else "none")
    )

    if not should_publish_today(force, now, progress):
        print(f"Skipping: today's Madrid date ({now.date().isoformat()}) is already completed.")
        return 0

    if force:
        print("Force mode: bypassing the Madrid daily publication guard.")
    else:
        print(f"Publishing: no successful lesson exists for Madrid date {now.date().isoformat()}.")

    # The legacy sender still contains its old exact-hour guard. Passing force=True
    # here bypasses only that obsolete check; the wrapper above enforces the new
    # one-publication-per-Madrid-day rule for normal runs.
    return await publish_next_lesson(
        level=level,
        lessons_dir=lessons_dir,
        progress_path=progress_path,
        dry_run=dry_run,
        force=True,
        keep_artifacts=keep_artifacts,
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Publish the next A1 lesson with a Madrid daily publication guard."
    )
    parser.add_argument("--level", default=DEFAULT_LEVEL)
    parser.add_argument("--lessons-dir", type=Path, default=DEFAULT_LESSONS_DIR)
    parser.add_argument("--progress-path", type=Path, default=DEFAULT_PROGRESS_PATH)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Bypass the Madrid daily publication guard.")
    parser.add_argument("--keep-artifacts", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    configure_stdio()
    args = build_arg_parser().parse_args(argv)
    try:
        return asyncio.run(
            run_guarded(
                level=args.level.lower(),
                lessons_dir=args.lessons_dir,
                progress_path=args.progress_path,
                dry_run=args.dry_run,
                force=args.force,
                keep_artifacts=args.keep_artifacts,
            )
        )
    except SenderError as exc:
        print(f"telegram_daily_guarded error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

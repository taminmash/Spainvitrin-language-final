"""Tests for interactive lesson keyboard generation and publisher state handling."""

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from telegram_daily_sender import (
    build_lesson_keyboard,
    load_lessons,
    load_progress,
    next_lesson,
    publish_next_lesson,
    send_telegram_video,
)


ROOT = Path(__file__).resolve().parents[1]


class LessonKeyboardTests(unittest.TestCase):
    def test_keyboard_has_required_layout_labels_and_callback_data(self) -> None:
        keyboard = build_lesson_keyboard("a1", 1)

        self.assertEqual(
            [[button.text for button in row] for row in keyboard.inline_keyboard],
            [
                ["📚 آرشیو درس‌ها"],
                ["🧠 آزمون", "🤖 تمرین در ربات"],
                ["👍 پسندیدم", "👎 نپسندیدم"],
                ["💬 ثبت نظر", "🚨 گزارش"],
            ],
        )
        self.assertEqual(
            [[button.callback_data for button in row] for row in keyboard.inline_keyboard],
            [
                ["lesson:archive:a1:1"],
                ["lesson:quiz:a1:1", "lesson:practice:a1:1"],
                ["lesson:react:like:a1:1", "lesson:react:dislike:a1:1"],
                ["lesson:comment:a1:1", "lesson:report:a1:1"],
            ],
        )

    def test_callback_data_stays_within_telegram_limit(self) -> None:
        keyboard = build_lesson_keyboard("a1", 1)

        for row in keyboard.inline_keyboard:
            for button in row:
                self.assertLessEqual(len(button.callback_data.encode("utf-8")), 64)

    def test_sender_attaches_keyboard_as_reply_markup(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video_path = Path(tmp) / "lesson.mp4"
            video_path.write_bytes(b"test video")
            bot = MagicMock()
            bot.send_video = AsyncMock()

            with patch("telegram_daily_sender.Bot", return_value=bot):
                asyncio.run(
                    send_telegram_video(
                        "test-token",
                        "@vitrin",
                        video_path,
                        level="a1",
                        lesson_number=1,
                    )
                )

            reply_markup = bot.send_video.await_args.kwargs["reply_markup"]
            self.assertEqual(reply_markup.inline_keyboard[0][0].callback_data, "lesson:archive:a1:1")

    def test_invalid_level_or_lesson_number_is_rejected(self) -> None:
        with self.assertRaisesRegex(Exception, "Invalid lesson level"):
            build_lesson_keyboard("a1:invalid", 1)
        with self.assertRaisesRegex(Exception, "positive integer"):
            build_lesson_keyboard("a1", 0)
        with self.assertRaisesRegex(Exception, "64-byte limit"):
            build_lesson_keyboard("a1", int("9" * 60))

    def test_reset_progress_selects_lesson_one(self) -> None:
        lessons = load_lessons("a1", ROOT / "source_content")
        progress = load_progress(ROOT / "progress" / "a1_daily.json")

        self.assertEqual(progress, {"level": "a1", "last_published_lesson": 0, "history": []})
        self.assertEqual(next_lesson(lessons, progress).lesson_number, 1)

    def test_dry_run_does_not_modify_progress(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            progress_path = Path(tmp) / "a1_daily.json"
            original_progress = {"level": "a1", "last_published_lesson": 0, "history": []}
            progress_path.write_text(json.dumps(original_progress), encoding="utf-8")

            async def fake_video(_, work_dir: Path) -> Path:
                video_path = work_dir / "lesson.mp4"
                video_path.write_bytes(b"test video")
                return video_path

            with patch("telegram_daily_sender.create_lesson_video", new=AsyncMock(side_effect=fake_video)):
                result = asyncio.run(
                    publish_next_lesson(
                        level="a1",
                        lessons_dir=ROOT / "source_content",
                        progress_path=progress_path,
                        dry_run=True,
                        force=False,
                        keep_artifacts=False,
                    )
                )

            self.assertEqual(result, 0)
            self.assertEqual(json.loads(progress_path.read_text(encoding="utf-8")), original_progress)


if __name__ == "__main__":
    unittest.main()

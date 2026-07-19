"""Unit tests for the Madrid-calendar-day publication guard."""

import unittest
from datetime import datetime

from telegram_daily_sender import MADRID_TZ, last_successful_publication_date, should_publish_today


def progress_with_publication(timestamp: str) -> dict[str, object]:
    return {"history": [{"published_at_madrid": timestamp}]}


class DailyPublicationGuardTests(unittest.TestCase):
    def test_delayed_run_publishes_when_nothing_was_published_today(self) -> None:
        now = datetime(2026, 7, 18, 9, 58, tzinfo=MADRID_TZ)
        progress = progress_with_publication("2026-07-17T08:02:00+02:00")

        self.assertTrue(should_publish_today(False, now, progress))

    def test_second_run_on_same_madrid_date_skips(self) -> None:
        now = datetime(2026, 7, 18, 9, 58, tzinfo=MADRID_TZ)
        progress = progress_with_publication("2026-07-18T08:03:00+02:00")

        self.assertFalse(should_publish_today(False, now, progress))

    def test_next_madrid_date_publishes(self) -> None:
        now = datetime(2026, 7, 19, 8, 0, tzinfo=MADRID_TZ)
        progress = progress_with_publication("2026-07-18T09:58:00+02:00")

        self.assertTrue(should_publish_today(False, now, progress))

    def test_force_bypasses_same_day_guard(self) -> None:
        now = datetime(2026, 7, 18, 9, 58, tzinfo=MADRID_TZ)
        progress = progress_with_publication("2026-07-18T08:03:00+02:00")

        self.assertTrue(should_publish_today(True, now, progress))

    def test_latest_history_timestamp_is_compared_in_madrid(self) -> None:
        progress = {
            "history": [
                {"published_at_madrid": "2026-07-17T08:00:00+02:00"},
                {"published_at_madrid": "2026-07-18T00:30:00+00:00"},
            ]
        }

        self.assertEqual(last_successful_publication_date(progress).isoformat(), "2026-07-18")


if __name__ == "__main__":
    unittest.main()

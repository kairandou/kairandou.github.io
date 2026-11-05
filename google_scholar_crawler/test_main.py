import copy
from pathlib import Path
import signal
import tempfile
import unittest
from unittest.mock import patch

import main


def author_response() -> dict:
    return {
        "scholar_id": main.DEFAULT_SCHOLAR_ID,
        "name": "Kairan Dou",
        "citedby": 201,
        "publications": [
            {
                "author_pub_id": f"{main.DEFAULT_SCHOLAR_ID}:example",
                "num_citations": 159,
                "bib": {"title": "Example publication"},
            }
        ],
    }


class SnapshotTests(unittest.TestCase):
    def test_deadline_bypasses_library_retry_handlers_and_restores_signal(self) -> None:
        original_handler = signal.getsignal(signal.SIGALRM)
        with self.assertRaisesRegex(SystemExit, "exceeded its deadline"):
            with main.fetch_deadline(10):
                try:
                    signal.raise_signal(signal.SIGALRM)
                except Exception:
                    self.fail("Deadline was swallowed by a broad retry handler")
        self.assertEqual(signal.getsignal(signal.SIGALRM), original_handler)

    def test_preserves_publication_contract_and_utc_timestamp(self) -> None:
        author = author_response()
        result = main.normalize_author(author, main.DEFAULT_SCHOLAR_ID)
        publication_id = f"{main.DEFAULT_SCHOLAR_ID}:example"
        self.assertEqual(result["publications"][publication_id]["num_citations"], 159)
        self.assertEqual(result["citedby"], 201)
        self.assertTrue(result["updated"].endswith("Z"))
        self.assertIsInstance(author["publications"], list)

    def test_rejects_empty_or_incomplete_author_response(self) -> None:
        for key, value in [
            ("publications", []),
            ("citedby", None),
            ("name", ""),
            ("scholar_id", "other"),
        ]:
            with self.subTest(key=key):
                author = author_response()
                author[key] = value
                with self.assertRaises(ValueError):
                    main.normalize_author(author, main.DEFAULT_SCHOLAR_ID)

    def test_rejects_invalid_counts_without_fabricating_zero(self) -> None:
        for value in [None, -1, "159", True]:
            with self.subTest(value=value):
                author = author_response()
                author["publications"][0]["num_citations"] = value
                with self.assertRaises(ValueError):
                    main.normalize_author(author, main.DEFAULT_SCHOLAR_ID)

    def test_accepts_a_verified_zero(self) -> None:
        author = author_response()
        author["publications"][0]["num_citations"] = 0
        result = main.normalize_author(author, main.DEFAULT_SCHOLAR_ID)
        self.assertEqual(
            next(iter(result["publications"].values()))["num_citations"], 0
        )

    def test_rejects_duplicate_or_wrong_author_publications(self) -> None:
        author = author_response()
        author["publications"].append(copy.deepcopy(author["publications"][0]))
        with self.assertRaises(ValueError):
            main.normalize_author(author, main.DEFAULT_SCHOLAR_ID)
        author = author_response()
        author["publications"][0]["author_pub_id"] = "other:example"
        with self.assertRaises(ValueError):
            main.normalize_author(author, main.DEFAULT_SCHOLAR_ID)

    def test_failed_fetch_preserves_last_good_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            for name in ("gs_data.json", "gs_data_shieldsio.json"):
                (output / name).write_text("previous valid snapshot")
            with patch.object(
                main, "fetch_author", side_effect=ValueError("empty response")
            ):
                with self.assertRaises(ValueError):
                    main.update_snapshot(main.DEFAULT_SCHOLAR_ID, output, 10)
            for name in ("gs_data.json", "gs_data_shieldsio.json"):
                self.assertEqual((output / name).read_text(), "previous valid snapshot")

    def test_serialization_failure_preserves_last_good_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            (output / "gs_data.json").write_text("previous valid snapshot")
            snapshot = main.normalize_author(author_response(), main.DEFAULT_SCHOLAR_ID)
            snapshot["unexpected"] = object()
            with self.assertRaises(TypeError):
                main.write_snapshot(snapshot, output)
            self.assertEqual(
                (output / "gs_data.json").read_text(), "previous valid snapshot"
            )

    def test_success_writes_both_compatible_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            snapshot = main.normalize_author(author_response(), main.DEFAULT_SCHOLAR_ID)
            main.write_snapshot(snapshot, output)
            import json

            self.assertEqual(
                json.loads((output / "gs_data.json").read_text())["citedby"], 201
            )
            self.assertEqual(
                json.loads((output / "gs_data_shieldsio.json").read_text())["message"],
                "201",
            )
            self.assertEqual(len(list(output.iterdir())), 2)


if __name__ == "__main__":
    unittest.main()

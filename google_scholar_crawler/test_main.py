import copy
from contextlib import redirect_stderr, redirect_stdout
import io
import json
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
        with self.assertRaisesRegex(
            main.FetchDeadlineExceeded, "exceeded its deadline"
        ):
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
            self.assertEqual(
                json.loads((output / "gs_data.json").read_text())["citedby"], 201
            )
            self.assertEqual(
                json.loads((output / "gs_data_shieldsio.json").read_text())["message"],
                "201",
            )
            self.assertEqual(len(list(output.iterdir())), 2)

    def test_cli_skips_unavailable_retrieval_without_changing_files(self) -> None:
        from httpx import ConnectError, ReadTimeout
        from scholarly import scholarly
        from scholarly._proxy_generator import MaxTriesExceededException

        failures = [
            (main, "fetch_author", main.FetchDeadlineExceeded("deadline exceeded")),
            (
                scholarly,
                "search_author_id",
                MaxTriesExceededException("Cannot Fetch from Google Scholar."),
            ),
            (scholarly, "search_author_id", ConnectError("connection interrupted")),
            (scholarly, "search_author_id", ReadTimeout("request timed out")),
        ]
        for target, method, error in failures:
            with self.subTest(error=type(error).__name__):
                with tempfile.TemporaryDirectory() as temporary:
                    output = Path(temporary)
                    old_snapshot = main.normalize_author(
                        author_response(), main.DEFAULT_SCHOLAR_ID
                    )
                    old_snapshot["updated"] = "2026-11-01T00:00:00Z"
                    main.write_snapshot(old_snapshot, output)
                    previous = {
                        path: (path.read_bytes(), path.stat().st_mtime_ns)
                        for path in output.iterdir()
                    }
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with (
                        patch.object(target, method, side_effect=error),
                        redirect_stdout(stdout),
                        redirect_stderr(stderr),
                    ):
                        result = main.main(["--output-dir", str(output)])
                    self.assertEqual(result, 75)
                    self.assertIn("refresh skipped", stderr.getvalue())
                    self.assertNotIn("Updated", stdout.getvalue() + stderr.getvalue())
                    self.assertEqual(set(output.iterdir()), set(previous))
                    for path, (content, modified) in previous.items():
                        self.assertEqual(path.read_bytes(), content)
                        self.assertEqual(path.stat().st_mtime_ns, modified)

    def test_cli_skipped_retrieval_does_not_create_an_empty_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "absent"
            with (
                patch.object(
                    main,
                    "fetch_author",
                    side_effect=main.ScholarUnavailable("unavailable"),
                ),
                redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(main.main(["--output-dir", str(output)]), 75)
            self.assertFalse(output.exists())

    def test_cli_does_not_swallow_programming_errors_or_regular_exit(self) -> None:
        for error in (
            TypeError("bug"),
            ValueError("invalid"),
            OSError("I/O"),
            SystemExit(12),
        ):
            with self.subTest(error=type(error).__name__):
                with patch.object(main, "fetch_author", side_effect=error):
                    with self.assertRaises(type(error)):
                        main.main([])

    def test_cli_validation_failure_is_not_an_unavailable_result(self) -> None:
        from scholarly import scholarly

        author = author_response()
        author["publications"] = []
        with (
            patch.object(scholarly, "search_author_id", return_value=author),
            patch.object(scholarly, "fill"),
            patch.object(main, "write_snapshot") as writer,
        ):
            with self.assertRaisesRegex(ValueError, "no publication list"):
                main.main([])
            writer.assert_not_called()

    def test_cli_write_and_serialization_errors_remain_failures(self) -> None:
        snapshot = main.normalize_author(author_response(), main.DEFAULT_SCHOLAR_ID)
        with (
            patch.object(main, "fetch_author", return_value=snapshot),
            patch.object(
                main, "write_snapshot", side_effect=PermissionError("read-only")
            ),
        ):
            with self.assertRaises(PermissionError):
                main.main([])
        snapshot["unexpected"] = object()
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "absent"
            with patch.object(main, "fetch_author", return_value=snapshot):
                with self.assertRaises(TypeError):
                    main.main(["--output-dir", str(output)])
            self.assertFalse(output.exists())

    def test_cli_success_returns_zero_after_writing_snapshot(self) -> None:
        snapshot = main.normalize_author(author_response(), main.DEFAULT_SCHOLAR_ID)
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary)
            stdout = io.StringIO()
            with (
                patch.object(main, "fetch_author", return_value=snapshot),
                redirect_stdout(stdout),
            ):
                result = main.main(["--output-dir", str(output)])
            self.assertEqual(result, 0)
            self.assertIn("Updated 1 publications", stdout.getvalue())
            self.assertEqual(
                json.loads((output / "gs_data.json").read_text()), snapshot
            )


if __name__ == "__main__":
    unittest.main()

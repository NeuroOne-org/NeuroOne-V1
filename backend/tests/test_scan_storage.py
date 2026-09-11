"""Tests for LocalScanStorage (ADR-006 decision 5)."""

from uuid import uuid4

from app.storage.scan_storage import LocalScanStorage


def test_save_persists_the_exact_bytes(tmp_path) -> None:
    storage = LocalScanStorage(tmp_path)
    visit_id = uuid4()

    key = storage.save(visit_id, "scan.dcm", b"scan-bytes")

    assert (tmp_path / key).read_bytes() == b"scan-bytes"


def test_two_uploads_for_the_same_visit_never_collide(tmp_path) -> None:
    storage = LocalScanStorage(tmp_path)
    visit_id = uuid4()

    first = storage.save(visit_id, "scan.dcm", b"first")
    second = storage.save(visit_id, "scan.dcm", b"second")

    assert first != second
    assert (tmp_path / first).read_bytes() == b"first"
    assert (tmp_path / second).read_bytes() == b"second"


def test_a_path_traversal_filename_is_neutralized(tmp_path) -> None:
    """The filename is untrusted client input."""
    storage = LocalScanStorage(tmp_path)
    visit_id = uuid4()

    key = storage.save(visit_id, "../../etc/passwd", b"content")

    saved_path = (tmp_path / key).resolve()
    assert saved_path.is_relative_to(tmp_path.resolve())
    assert saved_path.read_bytes() == b"content"


def test_delete_removes_the_saved_file(tmp_path) -> None:
    storage = LocalScanStorage(tmp_path)
    visit_id = uuid4()
    key = storage.save(visit_id, "scan.dcm", b"content")

    storage.delete(key)

    assert not (tmp_path / key).exists()


def test_deleting_a_missing_key_is_not_an_error(tmp_path) -> None:
    storage = LocalScanStorage(tmp_path)

    storage.delete(f"{uuid4()}/does-not-exist")

from Browser.browser import _RFContextTracker


def test_fresh_tracker_returns_all_empty():
    tracker = _RFContextTracker()
    assert tracker.context() == {
        "suite_id": "",
        "suite_name": "",
        "test_id": "",
        "test_name": "",
    }


def test_after_start_suite_suite_fields_populated():
    tracker = _RFContextTracker()
    tracker.start_suite("s1", "Root Suite")
    assert tracker.context() == {
        "suite_id": "s1",
        "suite_name": "Root Suite",
        "test_id": "",
        "test_name": "",
    }


def test_after_start_suite_and_start_test_all_fields_present():
    tracker = _RFContextTracker()
    tracker.start_suite("s1", "Root Suite")
    tracker.start_test("s1-t1", "My Test")
    assert tracker.context() == {
        "suite_id": "s1",
        "suite_name": "Root Suite",
        "test_id": "s1-t1",
        "test_name": "My Test",
    }


def test_end_test_clears_test_fields_restores_suite():
    tracker = _RFContextTracker()
    tracker.start_suite("s1", "Root Suite")
    tracker.start_test("s1-t1", "My Test")
    tracker.end_test()
    assert tracker.context() == {
        "suite_id": "s1",
        "suite_name": "Root Suite",
        "test_id": "",
        "test_name": "",
    }


def test_end_suite_on_root_clears_all():
    tracker = _RFContextTracker()
    tracker.start_suite("s1", "Root Suite")
    tracker.end_suite()
    assert tracker.context() == {
        "suite_id": "",
        "suite_name": "",
        "test_id": "",
        "test_name": "",
    }


def test_nested_suites_restore_parent_on_end_suite():
    tracker = _RFContextTracker()
    tracker.start_suite("s1", "Root Suite")
    tracker.start_suite("s1-s1", "Child Suite")
    tracker.end_suite()
    assert tracker.context() == {
        "suite_id": "s1",
        "suite_name": "Root Suite",
        "test_id": "",
        "test_name": "",
    }

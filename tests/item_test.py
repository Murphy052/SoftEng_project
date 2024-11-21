from src.app.cases.managers.item import item_manager


def test_get_case_items():
    items = item_manager.get_case_items(case_id=1)

    assert len(items) == 2
    assert items[0].name == "AWP | Oni Taiji"
    assert items[1].name == "M4A4 | Hellfire"

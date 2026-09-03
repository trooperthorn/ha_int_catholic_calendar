"""translations/en.json is what Home Assistant loads at runtime for the UI.

This integration ships no strings.json, so there is nothing to diff against;
these tests instead pin translations/en.json to the step_id and abort
reason the config flow actually uses, since a file with no content check at
all was exactly the bug this session found (it lived at the component root
instead of translations/, so none of it ever reached users).
"""
import json
from pathlib import Path

COMPONENT_DIR = Path(__file__).parent.parent / "custom_components" / "catholic_calendar"


def load_translations() -> dict:
    return json.loads((COMPONENT_DIR / "translations" / "en.json").read_text())


def test_translations_file_exists_at_the_path_home_assistant_loads():
    assert (COMPONENT_DIR / "translations" / "en.json").is_file()


def test_user_step_has_a_title_and_description():
    step = load_translations()["config"]["step"]["user"]
    assert step["title"]
    assert step["description"]


def test_single_instance_abort_reason_is_translated():
    abort = load_translations()["config"]["abort"]
    assert "single_instance_allowed" in abort
    assert abort["single_instance_allowed"]

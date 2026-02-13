from __future__ import annotations

import pytest

from nmap_scanning_tool.errors import ValidationError
from nmap_scanning_tool.profiles import get_profile, list_profiles


def test_list_profiles_has_expected_order_and_size() -> None:
    profiles = list_profiles()
    assert len(profiles) == 12
    assert profiles[0].profile_id == "1"
    assert profiles[-1].profile_id == "12"


def test_get_profile_returns_custom_profile() -> None:
    profile = get_profile("12")
    assert profile.supports_custom_args is True
    assert profile.arguments == ()


def test_get_profile_rejects_unknown_profile() -> None:
    with pytest.raises(ValidationError):
        get_profile("99")

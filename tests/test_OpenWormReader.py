import logging

import pytest

from c302.OpenWormReader import format_muscle_name


class TestFormatMuscleName:
    @pytest.mark.parametrize(
        "name, name_expected, log_count_expected",
        [("ADER", "ADER", 1), ("MVL01", "MVL01", 0)],
    )
    def test_should_log_unknown_name_format(
        self, name: str, name_expected: str, log_count_expected: int, caplog
    ) -> None:
        caplog.set_level(logging.DEBUG)

        format_muscle_name(name)

        assert (
            len(caplog.records) == log_count_expected
        ), f"The incorrect quantity of logs was recorded."

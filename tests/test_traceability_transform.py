from scripts.traceability_transform import (
    normalize_configuration,
    normalize_module_name,
    normalize_part_number,
)


def test_normalize_part_number_handles_common_formats() -> None:
    assert normalize_part_number("P1001") == "P-1001"
    assert normalize_part_number("P-1001") == "P-1001"
    assert normalize_part_number("p_1001") == "P-1001"
    assert normalize_part_number("p 1001") == "P-1001"


def test_normalize_configuration_handles_common_formats() -> None:
    assert normalize_configuration("Config A Rev2") == "CFG-A-REV-2"
    assert normalize_configuration("CFG-A / Rev 2") == "CFG-A-REV-2"
    assert normalize_configuration("cfg_a_rev_2") == "CFG-A-REV-2"
    assert normalize_configuration("A-R2") == "CFG-A-REV-2"


def test_normalize_module_name_handles_common_aliases() -> None:
    assert normalize_module_name("PCM") == "power_control_module"
    assert normalize_module_name("Power Ctrl Mod") == "power_control_module"
    assert normalize_module_name("Power Control Module") == "power_control_module"
    assert normalize_module_name("power control module") == "power_control_module"


def test_normalize_module_name_handles_unknown_module_names() -> None:
    assert normalize_module_name("Thermal-Control Unit") == "thermal_control_unit"
from nrobo.exceptions import IncorrectVersion, InvalidOperation
from nrobo.util.version import Version


class TestVersionPkg:

    def test_version_class_properties(self):
        """Validate Version class property @major"""

        major = 2024
        minor = 6
        patch = 1

        version = Version(f"{major}.{minor}.{patch}")

        assert version.major == major
        assert version.minor == minor
        assert version.patch == patch
        assert version.major_next == major + 1
        assert version.major_prev == major - 1
        assert version.patch_next == patch + 1
        assert version.patch_prev == patch - 1
        assert version.version == f"{major}.{minor}.{patch}"
        assert version.version_next == f"{major}.{minor}.{patch + 1}"
        assert version.version_prev == f"{major}.{minor}.{patch - 1}"
        assert version.major_incremented() == f"{major + 1}.{minor}.{patch}"
        assert version.major_decremented() == f"{major - 1}.{minor}.{patch}"
        assert version.minor_incremented() == f"{major}.{minor + 1}.{patch}"
        assert version.minor_decremented() == f"{major}.{minor - 1}.{patch}"
        assert version.patch_incremented() == f"{major}.{minor}.{patch + 1}"
        assert version.patch_decremented() == f"{major}.{minor}.{patch - 1}"
        assert version.version_incremented() == f"{major}.{minor}.{patch + 1}"
        assert version.version_decremented() == f"{major}.{minor}.{patch - 1}"

        try:
            Version("2010.d.45")
            assert False
        except IncorrectVersion as e:
            assert True

    def test_arithmetic_operations_on_Version_class(self):

        major = 2024
        minor = 6
        patch = 1

        version_1 = Version(f"{major}.{minor}.{patch + 2}")
        version_2 = Version(f"{major}.{minor}.{patch + 1}")

        assert version_1 > version_2
        assert version_2 < version_1

        version_1 = version_2

        assert version_1 == version_2

        try:
            assert version_1 > 2
            assert False
        except InvalidOperation as e:
            assert True

        try:
            assert version_1 < 2
            assert False
        except InvalidOperation as e:
            assert True

        version_1 = Version(f"{major}.{minor}.{patch}")
        version_2 = Version(f"{major}.{minor}.{patch + 1}")
        version_3 = Version(f"{major}.{minor}.{patch + 2}")

        assert version_1 + 1 == version_2
        assert version_3 - 1 == version_2

        assert version_2 + 1 <= version_3
        assert version_3 >= version_2 + 1

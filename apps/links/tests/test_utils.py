import pytest
from ..utils import generate_random_short_code, is_valid_short_code_name

class TestLinkUtils:
    def test_generate_random_short_code_is_alphanumeric(self):
        """
        GIVEN a call to generate_random_short_code function
        WHEN a short code is generated
        THEN it should return a string of alphanumerical characters
        """
        result = generate_random_short_code(7)
        assert result.isalnum()

    def test_generate_random_short_code_raises_error_for_invalid_input(self):
        """
        GIVEN an invalid argument type or negative number
        WHEN generate_random_short_code function is called
        THEN raises ValueError
        """
        with pytest.raises(ValueError, match='type'):
            generate_random_short_code('11')

        with pytest.raises(ValueError, match='greater than 0'):
            generate_random_short_code(-1)

    def test_valid_short_code_returns_true(self):
        assert is_valid_short_code_name('valid-short_Code') == True

    def test_invalid_short_code_returns_false(self):
        assert is_valid_short_code_name('valid+short?Code') == False
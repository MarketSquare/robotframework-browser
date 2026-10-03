---
name: write-python-unit-tests
description: 'Write Python unit tests for Python code. Use when: creating new tests, improving test coverage, testing functions or classes in isolation, writing test cases for edge cases, or following TDD practices.'
applyTo: 'utest/**'
---
# Write Python Unit Tests
Python unit tests must always be written in the `utest` folder and using pytest.

Unit tests must be readable and maintainable. They should test one thing at a time, and be easy to understand. Use descriptive names for test functions and variables.

Linting must be done by calling `inv lint-python --fix` to ensure consistent formatting and style.

## Example

```python
@pytest.fixture(scope="module")
def cookie():
    return Cookie(None)


def test_cookie_as_dot_dict_expiry(cookie: Cookie):
    epoch = 1604698517
    data = cookie._cookie_as_dot_dict({"expires": epoch})
    assert data.expires == datetime.fromtimestamp(epoch, tz=timezone.utc)
```

# Assertions
Use `assert` statements to check the expected outcomes of the code being tested. If there need to
assert longer data structures, use approval tests. When test are run, ask user to look the
approval test file and approve it if the data structure is correct. If the data structure is incorrect, ask user to update the approval test file with the correct data structure and re-run the tests.

# Running unit tests
Unit tests can be run with `invoke`:

```bash
inv utest
```

# Thing to avoid
Because must test are readable, avoid comments or docstrings that explain what the test is doing.
The test should be self-explanatory. If you find yourself needing to explain what the test is
doing, consider refactoring the test to make it more readable. If there are complex data
structures, consider using helper functions or fixtures to set up the test data in a more
readable way or adding comments on the key point of the data structure.

# QA Automation Infra

### This is an example of a working code infra for QA Automation using Python and PyTest framework.

## Structure

* ***qa_classes*** - declares a set of classes that aim to model test cases of features, test suites that contain
  certain features, errors, exceptions and more.

* ***qa_methods*** - contains a set of various methods to be used in the automation workflow. Some are purely technical,
  like extracting the specific tests by category or by test suite name
* Others are helper methods to catch and assert errors and exceptions (useful for negative testing)
* ***qa_test_suites*** - JSON formatted file that contains a list of test suites. Each suite is defined with child
  features that will be tested in each test. Each test case also has conditions which consts of errors and exceptions to
  be expected, a category it belongs to to help categorize and organize tests, a Skip boolean if we wish to skip a test
  for any reason, and a Bug string which will be printed in CI if the test is skipped due to a bug
* ***utils*** - contains misc. utils, cleaners and waiters

## Aim and basic flow

The goal is to model tests and allowing to quickly add, change or remove tests that share some common logic simply by
using the qa_test_suites.py file, with their expected errors, conditions etc. While also allowing flexibility by marking
specific tests to be skipped if needed for any reason.

When a test session begins, the methods in qa_methods.py are responsible for extracting the tests and data from the
qa_test_suites.py file, then later PyTest executes the tests returned according to the category or test suite name, with
it's respected test cases, their conditions, expected behavior etc.. 
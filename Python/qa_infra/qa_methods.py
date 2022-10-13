import pytest
from qa_infra.qa_test_suites import test_suites
from datetime import timedelta
from utils import ErrorUtils, AssertionHelper, Cleaner, HttpException
from utils import CommonWaiters as Cw

ADVANCED_FEATURE_TIMEOUT = 600


class QaMethods:
    @staticmethod
    def get_test_cases_from_suite(test_suite_name) -> list:
        test_cases = test_suites[test_suite_name]
        test_cases = [pytest.param(test_case, marks=pytest.mark.skip(reason=test_case["Bug"])) if (
                test_case["Skip"] is True) else test_case for test_case in test_cases]
        return test_cases

    @staticmethod
    def get_ids(test_suite_name) -> list:
        ids = []
        test_cases = test_suites[test_suite_name]
        for test_case in test_cases:
            ids.append(test_case["feature"])
        return ids

    @staticmethod
    def get_test_cases_from_category(category) -> list:
        suite_names = test_suites.keys()
        test_cases = [test_case for suite in suite_names for test_case in test_suites[suite] if
                      test_case["Category"] == category]
        test_cases = [pytest.param(test_case, marks=pytest.mark.skip(reason=test_case["Bug"])) if (
                test_case["Skip"] is True) else test_case for test_case in test_cases]
        return test_cases

    @staticmethod
    def get_ids_from_category(category) -> list:
        suite_names = test_suites.keys()
        ids = [test_case["feature"] for suite in suite_names for test_case in test_suites[suite] if
               test_case["Category"] == category]
        return ids

    @staticmethod
    def assert_advanced_feature_errors(advanced_feature_details, expected_errors):
        advanced_feature_errors = [error.code for error in advanced_feature_details.errors]
        expected_advanced_feature_errors = [error.code for error in expected_errors]
        AssertionHelper.collections_equal(advanced_feature_errors, expected_advanced_feature_errors)

    @staticmethod
    def assert_exception(exception, expected_exception):
        exception_error_codes = ErrorUtils.get_exception_error_codes(exception)
        assert exception.status_code == expected_exception.status_code
        AssertionHelper.collections_equal(exception_error_codes, expected_exception.error_codes)

    @staticmethod
    def catch_launch_advanced_feature_exception(api, feature):
        api.do_something_with_feature(feature_name=feature)
        with pytest.raises(HttpException) as e:
            advanced_feature = api.start_advanced_feature(advanced_feature_name=feature, feature_name=feature,
                                        duration=timedelta(hours=1))
            with Cleaner(api) as cleaner:
                cleaner.add_advanced_feature(advanced_feature_id=advanced_feature.advanced_feature_id)
                waiter = Cw(api)
                waiter.wait_until_advanced_feature_not_waiting(advanced_feature_id=advanced_feature.advanced_feature_id, max_retries=10)
                pytest.fail(msg="Sandbox launched, expected it to fail")
        return e.value

    @staticmethod
    def catch_launch_advanced_feature_errors(api, feature):
        advanced_feature = api.start_advanced_feature(advanced_feature_name=feature, feature_name=feature,
                                    duration=timedelta(hours=1))
        with Cleaner(api) as cleaner:
            cleaner.add_advanced_feature(advanced_feature_id=advanced_feature.advanced_feature_id)
            waiter = Cw(api)
            waiter.wait_until_advanced_feature_deployed_with_errors(advanced_feature_id=advanced_feature.advanced_feature_id,
                                                           max_seconds=ADVANCED_FEATURE_TIMEOUT)
            advanced_feature_details = api.get_advanced_feature_details(advanced_feature.advanced_feature_id)
            return advanced_feature_details

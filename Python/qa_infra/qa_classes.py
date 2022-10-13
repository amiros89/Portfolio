class Testcase:
    def __init__(self, testcase):
        self.conditions = TestConditions(testcase["conditions"])
        self.bug = testcase["Bug"]
        self.skip = testcase["Skip"]


class TestCaseWithFeature(Testcase):
    def __init__(self, testcase):
        super(TestCaseWithFeature, self).__init__(testcase)
        self.feature = testcase["feature"]


class TestCaseWithAdvancedFeature(TestCaseWithFeature):
    def __init__(self, testcase):
        super(TestCaseWithAdvancedFeature, self).__init__(testcase)
        self.expected_advanced_feature_status = testcase["advanced_feature_status"]


class ExpectedAdvancedFeatureError:
    def __init__(self, code):
        self.code = code


class ExpectedException:
    def __init__(self, status_code, error_codes):
        self.status_code = status_code
        self.error_codes = error_codes


class TestConditions:
    def __init__(self, conditions):
        self.advanced_feature_errors = conditions["advanced_feature_errors"]
        self.exceptions = conditions["exceptions"]
        
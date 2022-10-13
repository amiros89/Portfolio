class ErrorUtils:
    # some error handling utils
    @staticmethod
    def get_exception_error_codes(exception):
        pass


class AssertionHelper:
    # code that helps with assertions
    @staticmethod
    def collections_equal(col1, col2):
        pass

    pass


class Cleaner:
    # code that is responsible for cleaning up after tests
    def __init__(self, arg):
        pass


class CommonWaiters:
    # waiters for conditions
    def __init__(self, arg):
        pass

    def wait_until_advanced_feature_not_waiting(self, advanced_feature_id, max_retries):
        pass
    def wait_until_advanced_feature_deployed_with_errors(self,advanced_feature_id, max_seconds):
        pass

class HttpException:
    # Exception that API returns when something unexpected happens
    pass

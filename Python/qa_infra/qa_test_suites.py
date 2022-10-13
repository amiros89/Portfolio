from qa_infra.qa_classes import ExpectedSandboxError, ExpectedException

test_suites = {
    "test_suite_1": [
        {
            "feature": "feature1",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=["InvalidSomething"])]
                },
            "Bug": "Bug 4754: Something didn't work...",
            "Skip": True,
            "Category": "Feature Category"
        },
        {
            "feature": "feature2",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=["InvalidSomething"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        }
    ],
    "test_suite_2": [
        {
            "feature": "feature3",
            "feature_status": "ActiveWithError",
            "conditions":
                {
                    "feature_errors": [ExpectedSandboxError(code="CREATE_FAILED")],
                    "exceptions": []
                },
            "Bug": "Skipping test",
            "Skip": True,
            "Category": ""
        },
        {
            "feature": "feature4",
            "feature_status": "ActiveWithError",
            "conditions":
                {
                    "feature_errors": [ExpectedSandboxError(code="IMAGE_NOT_FOUND")],
                    "exceptions": []
                },
            "Bug": "Bug 4708: Redundant error message",
            "Skip": True,
            "Category": ""

        },
        {
            "feature": "feature5",
            "feature_status": "",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=422, error_codes=["InvalidSomethingElse"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": ""
        },
        {
            "feature": "feature6",
            "feature_status": "",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=422, error_codes=["InvalidSomethingElse"])]
                },
            "Bug": "Bug 4717: feature6 doesn't work",
            "Skip": True,
            "Category": ""
        },
        {
            "feature": "feature7",
            "feature_status": "",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=422, error_codes=["InvalidSomethingElse"])]
                },
            "Bug": "Bug 4716: feature7 takes a long time to load...",
            "Skip": True,
            "Category": ""
        }
    ],
    "test_suite_3": [
        {
            "feature": "feature_1",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=423, error_codes=["InvalidSomethingElse"])]
                },
            "Bug": "Bug 5082: Missing validation",
            "Skip": True,
            "Category": "Feature Category"

        },
        {
            "feature": "feature_2",
            "feature_status": "",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=["INVALID_INSTANCES_VALUE"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        },
        {
            "feature": "feature_3",
            "feature_status": "",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400,
                                                           error_codes=["feature_APPLICATION_WITH_TARGET_MUST_BE_"
                                                                        "SINGLE_INSTANCE"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        }
    ],
    "test_suite_4": [
        {
            "feature": "this_suite_feature1",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=["MISSING_DEPENDENCIES"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"

        },
        {
            "feature": "this_suite_feature2",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": []
                },
            "Bug": "Bug 5165: something terrible happened",
            "Skip": True,
            "Category": "Feature Category"

        }
    ],
    "test_several_similiar_use_cases": [
        {
            "feature": "use_case1",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=["INVALID_PORT_SYNTAX"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        },
        {
            "feature": "use_case2",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=["ERROR1",
                                                                                         "ERROR2"
                                                                                         ])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        }
    ],
    "test_other_use_cases": [
        {
            "feature": "feature1",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [ExpectedException(status_code=400, error_codes=[
                        "ERROR_CODE_NUMBER"])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        },
        {
            "feature": "feature2",
            "conditions":
                {
                    "feature_errors": [],
                    "exceptions": [
                        ExpectedException(status_code=400,
                                                error_codes=['ERROR_CODE_NUMBER'])]
                },
            "Bug": "",
            "Skip": False,
            "Category": "Feature Category"
        }
    ]
}
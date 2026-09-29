ROBUSTNESS_DATASET = [

    # -----------------------------------------------------
    # R01 — DIRECT QUESTION
    # -----------------------------------------------------

    {
        "id": "R01",

        "type": "direct",

        "question": (
            "What is Gram Sabha under Section 6?"
        ),

        "expected_section": "6",

        "should_be_supported": True
    },


    # -----------------------------------------------------
    # R02 — PARAPHRASED QUESTION
    # No section number is supplied.
    # -----------------------------------------------------

    {
        "id": "R02",

        "type": "paraphrased",

        "question": (
            "What matters are discussed in a "
            "Gram Sabha meeting?"
        ),

        "expected_section": "6",

        "should_be_supported": True
    },


    # -----------------------------------------------------
    # R03 — DIFFERENT WORDING
    # -----------------------------------------------------

    {
        "id": "R03",

        "type": "semantic",

        "question": (
            "What details should be submitted with "
            "an application for licensing a place "
            "for disposal of the dead?"
        ),

        "expected_section": "86",

        "should_be_supported": True
    },


    # -----------------------------------------------------
    # R04 — UNSUPPORTED QUESTION
    # -----------------------------------------------------

    {
        "id": "R04",

        "type": "unsupported",

        "question": (
            "How can I apply for an Indian passport?"
        ),

        "expected_section": None,

        "should_be_supported": False
    },


    # -----------------------------------------------------
    # R05 — EMPTY QUESTION
    # -----------------------------------------------------

    {
        "id": "R05",

        "type": "empty",

        "question": "",

        "expected_section": None,

        "should_be_supported": False
    }

]
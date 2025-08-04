TOKENS = {
    "sets": {
        "inline": [
            "jAvAsCriPt:",
        ],

        "trigger_exploits": [
            "alert()",
        ],

        "literal_tokens": [
            " ",
            ";",
            ",",
            "'",
            "/",
            "<!--",
            "-->",
            "--!>",
            "(",
            ")",
            "/*",
            "-",
            "`",
            "'",
            "\"",
            "*",
            "*/",
            "\r",
            "\n"
        ],

        "open": [          # 〈
            "<"
        ],

        "pre_token": [
            "/",
        ],

        "html_tokens": [
            "sCrIpT",
            "iMg",
            "sVg",
        ],

        "trigger_tokens": [
            "oNLoAd=",
            "oNeRrOr=",
            "OnBlUr=",
            "oNtOgGle="
        ],

        # will be directly closed
        "html_break_only_tokens": [
            "a",
            "bUtTon",
            "iNpUt",
            "frAmEsEt",
            "teMplAte",
            "auDio",
            "viDeO",
            "sOurCe",
            "hTmL",
            "nOeMbed",
            "noScRIpt",
            "StYle",
            "ifRaMe",
            "xMp",
            "texTarEa",
            "nOfRaMeS",
            "tITle",
        ],

        "pre_close": [
            "/",
        ],

        "close": [ 
            ">",
        ],
    },

    "trans": {
        "inline": ["inline", "trigger_exploits", "literal_tokens"],
        "open": ["html_tokens", "pre_token"],
        "pre_token": ["html_tokens", "html_break_only_tokens"],
        "html_tokens": ["literal_tokens", "trigger_tokens"],
        "html_break_only_tokens": ["close"],
        "pre_close": ["close"],
        "close": [],   # /* any */
        "html_breaker": [],   # /* any */
        "literal_tokens": [], # /* any */
        "pre_trigger_token": ["trigger_tokens"],
        "trigger_tokens": ["trigger_exploits", "literal_tokens"],
        "trigger_exploits": ["trigger_tokens", "pre_close", "close", "literal_tokens"],
    },
}


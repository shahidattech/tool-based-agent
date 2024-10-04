

tools = [
    {
        "type": "function",
        "function": {
            "name": "greet_user_after_introduction",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_type": {"type": "string"},
                    "name": {"type": "string"},
                },
                "required": ["customer_type", "name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "end_conversation",
            "strict": False,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_input",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_phone_numbers_by_name",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_otp",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {"type": "string"},
                },
                "required": ["phone_number"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "validate_otp",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "otp": {"type": "string"},
                    "name": {"type": "string"}, #take phone number instead of name
                },
                "required": ["otp", "name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_info_missing",
            "strict": False,
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                },
                "required": ["name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_doc_url", # change the dunction to dmv
            "strict": False,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_missing_info", # should accept a dict
            "strict": False,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "prompt_to_enter_customer_name",
            "description": "Prompt to enter customer name",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },

        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_dmv_document",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                },
                "required": ["customer_name"],
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_loan_options",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "cibil_score": {"type": "integer"},
                },
                "required": ["cibil_score"],
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "sign_document",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                },
                "required": ["customer_name"],
                "additionalProperties": False,
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "email_id": {"type": "string"},
                },
                "required": ["email_id"],
                "additionalProperties": False,
            }
        }
    }
]
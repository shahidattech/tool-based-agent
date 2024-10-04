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
        },
    },
    {
        "type": "function",
        "function": {
            "name": "end_conversation",
            "strict": False,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                },
                "required": ["customer_name"],
                "additionalProperties": False,
            },
        },
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
        },
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
        },
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
                    "name": {"type": "string"},  # take phone number instead of name
                },
                "required": ["otp", "name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_doc_url",  # change the dunction to dmv
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
            "name": "prompt_to_enter_customer_name",
            "description": "Prompt to enter customer name",
            "strict": True,
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
            "name": "generate_dmv_document",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                },
                "required": ["customer_name"],
                "additionalProperties": False,
            },
        },
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
            },
        },
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
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "print_signed_document",
            "strict": True,
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
            "name": "fetch_loan_options_for_dealer",
            "strict": True,
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
            "name": "verify_lender",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "lender_name": {"type": "string"},
                },
                "required": ["lender_name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_customers_deal_info",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                },
                "required": ["customer_name"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adjust_loan_coverage",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {"type": "string"},
                    "coverages": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                }
                    },
                },
                "required": ["customer_name", "coverages"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_customer_info",
            "strict": False,
            "parameters": {
                "type": "object",
                "properties": {
                    "existing_customer_name": {"type": "string"},
                    "full_name": {"type": "string"},
                    "address": {"type": "string"},
                    "policy": {
                        "type": "object",
                        "properties": {
                            "policy_no": {"type": "string"},
                            "effective_date": {"type": "string"},
                            "expiry_date": {"type": "string"},
                            "provider": {"type": "string"},
                        },
                        "required": [],
                        "additionalProperties": False,
                    },
                },
                "required": ["existing_customer_name"],
                "additionalProperties": False,
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_loan_options_for_customer_based_on_cibil_score",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "cibil_score": {"type": "integer"},
                },
                "required": ["cibil_score"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_loan_options_by_lender_and_cibil_score",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "lender_name": {"type": "string"},
                    "cibil_score": {"type": "integer"},
                },
                "required": ["lender_name", "cibil_score"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_all_supported_lender_names",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    }
]

# The customer update payload schema is like this -
#     {
#       "full_name": "John Doe",
#       "phone_primary": "555-555-0293",
#       "phone_secondary": "555-555-0294",
#       "address": "123 Oak Street..",
#       "policy": {
#         "policy_no": "1234567890",
#         "effective_date": "2023-01-01",
#         "expiry_date": "2024-01-01",
#         "provider": "ABC Insurance"
#       },
#       "vehicle": {
#         "vin": "12345678901234567",
#         "trim": "2023 Hyundai Santa Fe Limited Black",
#         "miles": 10000,
#         "color": "Red"
#       },
#       "trade_vehicle": {
#         "vin": "12345678901234567",
#         "trim": "2023 Hyundai Santa Fe Limited Black",
#         "miles": 10000,
#         "color": "Red"
#       },
#       "sale_price": "$10000",
#       "rebate": "$1000",
#       "dealer_fees": "$1000",
#       "trade_value": "$10000",
#       "trade_payoff": "$10000",
#       "tax_rate": 0.05,
#       "ssn": "123-45-6789",
#       "cibil_score": 700,
#       "customer_resdiential_info": {
#         "duration_of_living": 10,
#         "residence_type": "own",
#         "rent": "$1000"
#       },
#       "employee_info": {
#         "employment_type": "full_time",
#         "duration_of_employment": 10,
#         "organization": "ABC Company"
#       },
#       "monthly_income": "$10000",
#       "agreement": "Customer expects a payment below $700"
#     }

# write the schema as expected by the tool keeping in mind all fields are optional and default values are None or ""
# function to be called is update_customer_info

# {
#         "type": "function",
#         "function": {
#             "name": "update_customer_info",
#             "strict": False,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "full_name": {"type": "string"},
#                     "phone_primary": {"type": "string"},
#                     "phone_secondary": {"type": "string"},
#                     "address": {"type": "string"},
#                     "policy": {
#                         "type": "object",
#                         "properties": {
#                             "policy_no": {"type": "string"},
#                             "effective_date": {"type": "string"},
#                             "expiry_date": {"type": "string"},
#                             "provider": {"type": "string"},
#                         },
#                         "required": [],
#                         "additionalProperties": False,
#                     },
#                     "vehicle": {
#                         "type": "object",
#                         "properties": {
#                             "vin": {"type": "string"},
#                             "trim": {"type": "string"},
#                             "miles": {"type": "integer"},
#                             "color": {"type": "string"},
#                         },
#                         "required": [],
#                         "additionalProperties": False,
#                     },
#                     "trade_vehicle": {
#                         "type": "object",
#                         "properties": {
#                             "vin": {"type": "string"},
#                             "trim": {"type": "string"},
#                             "miles": {"type": "integer"},
#                             "color": {"type": "string"},
#                         },
#                         "required": [],
#                         "additionalProperties": False,
#                     },
#                     "sale_price": {"type": "string"},
#                     "rebate": {"type": "string"},
#                     "dealer_fees": {"type": "string"},
#                     "trade_value": {"type": "string"},
#                     "trade_payoff": {"type": "string"},
#                     "tax_rate": {"type": "number"},
#                     "ssn": {"type": "string"},
#                     "cibil_score": {"type": "integer"},
#                     "customer_resdiential_info": {
#                         "type": "object",
#                         "properties": {
#                             "duration_of_living": {"type": "integer"},
#                             "residence_type": {"type": "string"},
#                             "rent": {"type": "string"},
#                         },
#                         "required": [],
#                         "additionalProperties": False,
#                     },
#                     "employee_info": {
#                         "type": "object",
#                         "properties": {
#                             "employment_type": {"type": "string"},
#                             "duration_of_employment": {"type": "integer"},
#                             "organization": {"type": "string"},
#                         },
#                         "required": [],
#                         "additionalProperties": False,
#                     },
#                     "monthly_income": {"type": "string"},
#                     "agreement": {"type": "string"},
#                 },
#                 "required": [],
#                 "additionalProperties": False,
#             },
#         },
#     },

# {
#         "type": "function",
#         "function": {
#             "name": "update_missing_info",  # should accept a dict
#             "strict": False,
#             "parameters": {
#                 "type": "object",
#                 "properties": {},
#                 "required": [],
#                 "additionalProperties": False,
#             },
#         },
#     },
# {
#         "type": "function",
#         "function": {
#             "name": "fetch_loan_options",
#             "strict": True,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "cibil_score": {"type": "integer"},
#                 },
#                 "required": ["cibil_score"],
#                 "additionalProperties": False,
#             },
#         },
#     },
# {
#         "type": "function",
#         "function": {
#             "name": "fetch_loan_options_for_customer_by_name_and_cibil_score",
#             "strict": True,
#             "parameters": {
#                 "type": "object",
#                 "properties": {"customer_name": {"type": "string"}},
#                 "required": ["customer_name"],
#                 "additionalProperties": False,
#             },
#         },
#     },
# {
#         "type": "function",
#         "function": {
#             "name": "fetch_loan_package_by_lender_and_customer_name",
#             "strict": True,
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "lender_name": {"type": "string"},
#                     "customer_name": {"type": "string"},
#                 },
#                 "required": ["customer_name", "lender_name"],
#                 "additionalProperties": False,
#             },
#         },
#     }
"""
Comprehensive edge case test data for hierarchical search validation.
These cases are designed to expose potential failures in the matching algorithm.
"""

import json

# Edge case data structures
EDGE_CASES = {
    # 1. NESTED ARRAYS (array of arrays)
    "nested_arrays": {
        "company": {
            "id": "e1",
            "name": "NestedArraysCo",
            "departments": [
                {
                    "name": "Engineering",
                    "employees": [
                        [  # Array within array
                            {"name": "Alice", "role": "Engineer"},
                            {"name": "Bob", "role": "Manager"}
                        ],
                        [
                            {"name": "Charlie", "role": "Lead"}
                        ]
                    ]
                }
            ]
        }
    },

    # 2. EMPTY ARRAYS
    "empty_arrays": {
        "company": {
            "id": "e2",
            "name": "EmptyArraysCo",
            "departments": [],  # Empty departments
            "locations": [
                {
                    "city": "NYC",
                    "employees": []  # Empty nested array
                }
            ]
        }
    },

    # 3. NULL/NONE VALUES
    "null_values": {
        "company": {
            "id": "e3",
            "name": "NullValuesCo",
            "departments": [
                {
                    "name": None,  # Null field
                    "budget": 100000,
                    "employees": None  # Null array
                }
            ],
            "locations": None
        }
    },

    "mixed_types": {
        "company": {
            "id": "e4",
            "name": "MixedTypesCo",
            "data": [
                "string_value",
                123,
                {"name": "object"},
                ["nested", "array"],
                True,
                None
            ]
        }
    },

    "deep_nesting": {
        "company": {
            "id": "e5",
            "name": "DeepNestingCo",
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "level6": {
                                    "level7": {
                                        "level8": {
                                            "level9": {
                                                "level10": {
                                                    "level11": {
                                                        "level12": {
                                                            "target": "deep_value",
                                                            "cat": "A1"
                                                        }
                                                    },
                                                    "level13": {
                                                        "target": "deep_value_rep",
                                                        "cat": "A2"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    },

    # 6. EMPTY OBJECTS
    "empty_objects": {
        "company": {
            "id": "e6",
            "name": "EmptyObjectsCo",
            "departments": [
                {},  # Empty object in array
                {
                    "name": "Engineering",
                    "metadata": {}  # Empty nested object
                }
            ]
        }
    },

    # 7. BOOLEAN VALUES
    "boolean_values": {
        "company": {
            "id": "e7",
            "name": "BooleanCo",
            "departments": [
                {
                    "name": "Engineering",
                    "active": True,
                    "archived": False,
                    "employees": [
                        {"name": "Alice", "remote": True},
                        {"name": "Bob", "remote": False}
                    ]
                }
            ]
        }
    },

    # 8. NUMBER VS STRING
    "number_vs_string": {
        "company": {
            "id": "e8",
            "name": "NumberStringCo",
            "departments": [
                {
                    "name": "Engineering",
                    "budget": 100000,  # Number
                    "code": "100000"   # String that looks like number
                }
            ],
            "employee_count": 50,
            "employee_code": "50"
        }
    },

    "primitive_arrays": {
        "company": {
            "id": "e9",
            "name": "PrimitiveArraysCo",
            "tags": ["tech", "startup", "ai"],
            "ratings": [4.5, 4.8, 5.0],
            "features": [True, False, True]
        }
    },

    "special_chars": {
        "company": {
            "id": "e10",
            "name": "Special!@#$%Co",
            "departments": [
                {
                    "name": "R&D",
                    "location": "San Francisco, CA",
                    "email": "contact@company.com",
                    "description": "Multi-line\ntext with\ttabs"
                }
            ]
        }
    },

    "unicode_chars": {
        "company": {
            "id": "e11",
            "name": "UnicödeCø 世界 🌍",
            "departments": [
                {
                    "name": "Engïneérîng",
                    "employees": [
                        {"name": "Müller", "role": "Engineer"},
                        {"name": "José", "role": "Manager"},
                        {"name": "李明", "role": "Lead"}
                    ]
                }
            ],
            "locations": [
                {"city": "Zürich", "country": "Switzerland"},
                {"city": "São Paulo", "country": "Brazil"},
                {"city": "北京", "country": "China"}
            ]
        }
    },

    "large_arrays": {
        "company": {
            "id": "e12",
            "name": "LargeArraysCo",
            "departments": [
                {
                    "name": "Engineering",
                    "employees": [
                        {"name": f"Employee_{i}", "role": "Engineer"}
                        for i in range(1000)
                    ]
                }
            ]
        }
    },

    "duplicate_field_names": {
        "company": {
            "id": "e13",
            "name": "DuplicateFieldsCo",
            "departments": [
                {
                    "name": "Engineering",
                    "employees": [
                        {"name": "Alice"},
                        {"name": "Bob"}
                    ],
                    "projects": [
                        {"name": "Project Alpha"}
                    ]
                }
            ]
        }
    },

    "single_element_arrays": {
        "company": {
            "id": "e14",
            "name": "SingleElementCo",
            "departments": [
                {
                    "name": "Engineering",
                    "employees": [
                        {"name": "Alice", "role": "Engineer"}
                    ]
                }
            ],
            "locations": [
                {"city": "NYC", "country": "USA"}
            ]
        }
    },

    "inconsistent_structure": {
        "company": {
            "id": "e15",
            "name": "InconsistentCo",
            "departments": [
                {
                    "name": "Engineering",
                    "budget": 100000,
                    "employees": [
                        {"name": "Alice", "role": "Engineer", "salary": 120000}
                    ]
                },
                {
                    "name": "Sales",
                    "employees": [
                        {"name": "Bob"}
                    ]
                },
                {
                    "title": "Marketing",
                    "team": []
                }
            ]
        }
    },

    "numeric_edge_cases": {
        "company": {
            "id": "e16",
            "name": "NumericEdgeCo",
            "departments": [
                {
                    "name": "Finance",
                    "budget": 0,
                    "profit": -50000,
                    "employees": [
                        {
                            "name": "Alice",
                            "salary": 0,
                            "performance": -1
                        }
                    ]
                }
            ]
        }
    },

    "whitespace_values": {
        "company": {
            "id": "e17",
            "name": "  Whitespace Co  ",
            "departments": [
                {
                    "name": "",
                    "employees": [
                        {"name": "   ", "role": "Engineer"},
                        {"name": "\t\n", "role": "Manager"}
                    ]
                }
            ]
        }
    },

    "complex_nesting": {
        "company": {
            "id": "e18",
            "name": "ComplexNestingCo",
            "matrix": [
                [
                    [
                        {"x": 0, "y": 0, "z": 0},
                        {"x": 0, "y": 0, "z": 1}
                    ],
                    [
                        {"x": 0, "y": 1, "z": 0},
                        {"x": 0, "y": 1, "z": 1}
                    ]
                ]
            ]
        }
    },

    "query_ambiguity": {
        "company": {
            "id": "e19",
            "name": "AmbiguityCo",
            "employees": [
                {"name": "Alice", "department": "Engineering"}
            ],
            "departments": [
                {
                    "name": "Engineering",
                    "employees": [
                        {"name": "Bob", "role": "Engineer"}
                    ]
                }
            ]
        }
    },

    "floating_point": {
        "company": {
            "id": "e20",
            "name": "FloatingPointCo",
            "departments": [
                {
                    "name": "Finance",
                    "budget": 123456.789,
                    "tax_rate": 0.15,
                    "employees": [
                        {
                            "name": "Alice",
                            "salary": 100000.50,
                            "bonus_multiplier": 1.5
                        }
                    ]
                }
            ]
        }
    }
}


def generate_edge_case_queries():
    return {
        "nested_arrays_query": {
            "departments": {
                "name": "Engineering",
                "employees": {"name": "Alice"}
            }
        },

        "empty_arrays_query": {
            "departments": {"name": "Engineering"}
        },

        "null_values_query": {
            "departments": {"name": None}
        },

        "boolean_query": {
            "departments": {"active": True}
        },

        "number_query": {
            "departments": {"budget": 100000}
        },
        "string_query": {
            "departments": {"budget": "100000"}
        },

        "deep_nesting_query": {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "level6": {
                                    "level7": {
                                        "level8": {
                                            "level9": {
                                                "level10": {
                                                    "level11": {
                                                        "level12": {
                                                            "target": "deep_value"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },

        "primitive_array_query": {
            "tags": "tech"
        },

        "unicode_query": {
            "departments": {"name": "Engïneérîng"}
        },

        "whitespace_query": {
            "name": "  Whitespace Co  "
        },

        "zero_query": {
            "departments": {"budget": 0}
        }
    }


if __name__ == "__main__":
    print("=" * 80)
    print("EDGE CASE DATA STRUCTURES")
    print("=" * 80)

    for case_name, data in EDGE_CASES.items():
        print(f"\n{case_name.upper().replace('_', ' ')}:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
        print("..." if len(json.dumps(data)) > 500 else "")

    print("\n" + "=" * 80)
    print("EDGE CASE TEST QUERIES")
    print("=" * 80)

    queries = generate_edge_case_queries()
    for query_name, query in queries.items():
        print(f"\n{query_name}: {query}")


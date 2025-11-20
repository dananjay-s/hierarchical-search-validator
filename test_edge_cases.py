"""
Test runner for hierarchical search edge cases.
Identifies which edge cases cause failures in the current implementation.
"""

from multi_doc_validator import MultiDocumentValidator, Node, QueryNode, match_subtree
from edge_case_data import EDGE_CASES, generate_edge_case_queries
import json


class EdgeCaseTester:
    """Test edge cases against the hierarchical search implementation."""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.errors = 0

    def test_case(self, name, data, query, expected_match=None, description=""):
        """Test a single edge case."""
        print(f"\n{'=' * 80}")
        print(f"TEST: {name}")
        print(f"{'=' * 80}")
        if description:
            print(f"Description: {description}")

        print(f"\nData structure: {json.dumps(data, indent=2)[:300]}...")
        print(f"Query: {query}")

        try:
            # Create validator with single document
            documents = {"1": data}
            validator = MultiDocumentValidator(documents)

            # Execute query
            matches, twig_results = validator.execute_query(query)

            # Determine result
            has_match = len(matches) > 0

            if expected_match is None:
                status = "🔍 COMPLETED"
                result = "passed"
                self.passed += 1
            elif has_match == expected_match:
                status = "✓ PASSED"
                result = "passed"
                self.passed += 1
            else:
                status = "✗ FAILED"
                result = "failed"
                self.failed += 1

            print(f"\nResult: {status}")
            print(f"Matches: {matches}")
            print(f"Expected match: {expected_match}, Got: {has_match}")

            self.results.append({
                "name": name,
                "status": result,
                "matches": len(matches),
                "error": None
            })

        except Exception as e:
            print(f"\n✗ ERROR: {str(e)}")
            print(f"Exception type: {type(e).__name__}")
            self.results.append({
                "name": name,
                "status": "error",
                "matches": 0,
                "error": str(e)
            })
            self.errors += 1

    def run_all_tests(self):
        """Run all edge case tests."""
        print("\n" + "🧪" * 40)
        print("EDGE CASE TEST SUITE - HIERARCHICAL SEARCH")
        print("🧪" * 40)

        # Test 1: Nested arrays (array of arrays)
        self.test_case(
            "Nested Arrays (Array of Arrays)",
            EDGE_CASES["nested_arrays"],
            {"departments": {"name": "Engineering", "employees": {"name": "Alice"}}},
            expected_match=True,
            description="Can the algorithm handle employees as [[{...}]] instead of [{...}]?"
        )

        # Test 2: Empty arrays
        self.test_case(
            "Empty Arrays",
            EDGE_CASES["empty_arrays"],
            {"departments": {"name": "Engineering"}},
            expected_match=False,
            description="Does querying empty arrays cause errors?"
        )

        # Test 3: Null values
        self.test_case(
            "Null/None Values",
            EDGE_CASES["null_values"],
            {"departments": {"name": None}},
            expected_match=True,
            description="Can we query for null values?"
        )

        # Test 4: Mixed types in arrays
        self.test_case(
            "Mixed Types in Arrays",
            EDGE_CASES["mixed_types"],
            {"data": "string_value"},
            expected_match=False,
            description="How does the algorithm handle arrays with mixed types?"
        )

        # Test 5: Deep nesting (12 levels)
        deep_query = {
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
        }
        self.test_case(
            "Deep Nesting (12 levels)",
            EDGE_CASES["deep_nesting"],
            deep_query,
            expected_match=True,
            description="Performance and correctness with deeply nested structures"
        )

        # Test 6: Empty objects
        self.test_case(
            "Empty Objects",
            EDGE_CASES["empty_objects"],
            {"departments": {"name": "Engineering"}},
            expected_match=True,
            description="Empty objects in arrays should not break matching"
        )

        # Test 7: Boolean values
        self.test_case(
            "Boolean Values",
            EDGE_CASES["boolean_values"],
            {"departments": {"active": True}},
            expected_match=True,
            description="Can we match on boolean fields?"
        )

        # Test 8: Number vs string matching
        self.test_case(
            "Number vs String (Number Query)",
            EDGE_CASES["number_vs_string"],
            {"departments": {"budget": 100000}},
            expected_match=True,
            description="Query with number should match number field"
        )

        self.test_case(
            "Number vs String (String Query)",
            EDGE_CASES["number_vs_string"],
            {"departments": {"code": "100000"}},
            expected_match=True,
            description="Query with string should match string field"
        )

        self.test_case(
            "Number vs String (Cross-type Query)",
            EDGE_CASES["number_vs_string"],
            {"departments": {"budget": "100000"}},
            expected_match=False,
            description="String query should NOT match number field (type mismatch)"
        )

        # Test 9: Arrays of primitives
        self.test_case(
            "Arrays of Primitives (Strings)",
            EDGE_CASES["primitive_arrays"],
            {"tags": "tech"},
            expected_match=False,
            description="Can we match elements within primitive arrays?"
        )

        # Test 10: Special characters
        self.test_case(
            "Special Characters",
            EDGE_CASES["special_chars"],
            {"departments": {"name": "R&D"}},
            expected_match=True,
            description="Special characters in values should work"
        )

        # Test 11: Unicode characters
        self.test_case(
            "Unicode Characters",
            EDGE_CASES["unicode_chars"],
            {"departments": {"name": "Engïneérîng"}},
            expected_match=True,
            description="Unicode matching should work"
        )

        self.test_case(
            "Unicode Characters (Chinese)",
            EDGE_CASES["unicode_chars"],
            {"locations": {"city": "北京"}},
            expected_match=True,
            description="Chinese characters should match"
        )

        # Test 12: Large arrays (performance)
        self.test_case(
            "Large Arrays (1000 elements)",
            EDGE_CASES["large_arrays"],
            {"departments": {"employees": {"name": "Employee_500"}}},
            expected_match=True,
            description="Performance with large arrays"
        )

        # Test 13: Duplicate field names
        self.test_case(
            "Duplicate Field Names",
            EDGE_CASES["duplicate_field_names"],
            {"departments": {"name": "Engineering"}},
            expected_match=True,
            description="Multiple 'name' fields at different levels"
        )

        # Test 14: Single element arrays
        self.test_case(
            "Single Element Arrays",
            EDGE_CASES["single_element_arrays"],
            {"departments": {"employees": {"name": "Alice"}}},
            expected_match=True,
            description="Arrays with single element should work"
        )

        # Test 15: Inconsistent structure
        self.test_case(
            "Inconsistent Structure",
            EDGE_CASES["inconsistent_structure"],
            {"departments": {"name": "Engineering"}},
            expected_match=True,
            description="Departments with different schemas"
        )

        # Test 16: Zero and negative numbers
        self.test_case(
            "Zero Values",
            EDGE_CASES["numeric_edge_cases"],
            {"departments": {"budget": 0}},
            expected_match=True,
            description="Can we match zero values?"
        )

        self.test_case(
            "Negative Numbers",
            EDGE_CASES["numeric_edge_cases"],
            {"departments": {"profit": -50000}},
            expected_match=True,
            description="Can we match negative numbers?"
        )

        # Test 17: Whitespace values
        self.test_case(
            "Whitespace in Values",
            EDGE_CASES["whitespace_values"],
            {"name": "  Whitespace Co  "},
            expected_match=True,
            description="Exact match including whitespace"
        )

        self.test_case(
            "Empty String Values",
            EDGE_CASES["whitespace_values"],
            {"departments": {"name": ""}},
            expected_match=True,
            description="Can we match empty strings?"
        )

        # Test 18: Complex nesting patterns
        self.test_case(
            "Complex Nested Array Patterns (3D array)",
            EDGE_CASES["complex_nesting"],
            {"matrix": {"x": 0, "y": 0, "z": 0}},
            expected_match=True,
            description="3D array structure with objects"
        )

        # Test 19: Query ambiguity
        self.test_case(
            "Query Ambiguity (Multiple employee fields)",
            EDGE_CASES["query_ambiguity"],
            {"employees": {"name": "Alice"}},
            expected_match=True,
            description="Employees at root vs in departments"
        )

        # Test 20: Floating point numbers
        self.test_case(
            "Floating Point Numbers",
            EDGE_CASES["floating_point"],
            {"departments": {"budget": 123456.789}},
            expected_match=True,
            description="Exact floating point matching"
        )

        self.test_case(
            "Floating Point Precision",
            EDGE_CASES["floating_point"],
            {"departments": {"tax_rate": 0.15}},
            expected_match=True,
            description="Small floating point values"
        )

        # Print summary
        self._print_summary()

    def _print_summary(self):
        """Print test summary with detailed breakdown."""
        print("\n\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)

        total = self.passed + self.failed + self.errors

        print(f"\nTotal Tests: {total}")
        print(f"✓ Passed: {self.passed} ({100*self.passed/total if total > 0 else 0:.1f}%)")
        print(f"✗ Failed: {self.failed} ({100*self.failed/total if total > 0 else 0:.1f}%)")
        print(f"⚠ Errors: {self.errors} ({100*self.errors/total if total > 0 else 0:.1f}%)")

        print("\n" + "-" * 80)
        print("DETAILED RESULTS")
        print("-" * 80)

        for result in self.results:
            if result["status"] == "passed":
                symbol = "✓"
            elif result["status"] == "failed":
                symbol = "✗"
            else:
                symbol = "⚠"

            print(f"{symbol} {result['name']}")
            if result["error"]:
                print(f"  Error: {result['error']}")

        # Identify critical failures
        print("\n" + "-" * 80)
        print("CRITICAL EDGE CASES TO FIX")
        print("-" * 80)

        critical = [r for r in self.results if r["status"] in ["failed", "error"]]
        if critical:
            for i, result in enumerate(critical, 1):
                print(f"{i}. {result['name']}")
                if result["error"]:
                    print(f"   → {result['error']}")
        else:
            print("None! All edge cases handled correctly. 🎉")

        print("=" * 80)


if __name__ == "__main__":
    tester = EdgeCaseTester()
    tester.run_all_tests()


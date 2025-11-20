import json
from typing import Any, List, Dict, Set, Tuple
from data_generator import CompanyDataGenerator

# ==================== CORE HIERARCHY STRUCTURES ====================

class Node:
    def __init__(self, key: str, value: Any):
        self.key = key
        self.value = value
        self.children: List['Node'] = []
        self._build_children()

    def _build_children(self):
        if isinstance(self.value, dict):
            for k, v in self.value.items():
                self.children.append(Node(k, v))
        elif isinstance(self.value, list):
            for i, v in enumerate(self.value):
                self.children.append(Node(f"{self.key}[{i}]", v))

    def __repr__(self):
        return f"Node({self.key}={type(self.value).__name__})"


class QueryNode:
    def __init__(self, key: str, condition: Any):
        self.key = key
        self.condition = condition
        self.children: List['QueryNode'] = []
        if isinstance(condition, dict):
            for k, v in condition.items():
                self.children.append(QueryNode(k, v))

    def __repr__(self):
        return f"QueryNode({self.key})"


# ==================== MATCHING ALGORITHMS ====================

def match_tree(data_node: Node, query_node: QueryNode) -> bool:
    if data_node.key.split("[")[0] != query_node.key:
        return False

    if not query_node.children:
        return data_node.value == query_node.condition

    if isinstance(data_node.value, list):
        return any(match_subtree(child, query_node) for child in data_node.children)

    for qchild in query_node.children:
        matching_children = [
            dchild for dchild in data_node.children
            if match_tree(dchild, qchild)
        ]
        if not matching_children:
            return False
    return True


def match_subtree(data_node: Node, query_node: QueryNode) -> bool:
    if match_tree(data_node, query_node):
        return True
    return any(match_subtree(child, query_node) for child in data_node.children)


# ==================== MULTI-DOCUMENT VALIDATION ====================

class MultiDocumentValidator:
    """Validator for querying across multiple documents."""

    def __init__(self, documents: Dict[str, Dict[str, Any]]):
        """
        Initialize validator with a collection of documents.

        Args:
            documents: Dict[doc_id -> {document_data}]
        """
        self.documents = documents
        self.total_docs = len(documents)

    def process_query_twigs(self, query_dict: dict) -> List[Set[str]]:
        """
        Process a multi-twig query across all documents.
        Returns results for each twig independently.

        Args:
            query_dict: Dictionary where each key-value pair is a twig

        Returns:
            List of sets, each containing doc IDs that match the twig
        """
        twig_results = []

        for twig_key, twig_condition in query_dict.items():
            matching_docs = set()
            query_tree = QueryNode(twig_key, twig_condition)

            for doc_id, doc_data in self.documents.items():
                # Handle both raw document and wrapped structure
                data_structure = doc_data.get("company", doc_data)
                data_tree = Node("root", data_structure)

                if match_subtree(data_tree, query_tree):
                    matching_docs.add(doc_id)

            twig_results.append(matching_docs)

        return twig_results

    def intersect_results(self, twig_results: List[Set[str]]) -> Set[str]:
        """
        Intersect results from multiple twigs.
        Returns only documents that match ALL twigs.

        Args:
            twig_results: List of sets, each containing doc IDs

        Returns:
            Set of doc IDs that match all twigs
        """
        if not twig_results:
            return set()

        result = twig_results[0].copy()
        for twig_set in twig_results[1:]:
            result &= twig_set

        return result

    def union_results(self, twig_results: List[Set[str]]) -> Set[str]:
        """
        Union results from multiple twigs.
        Returns documents that match ANY twig (OR operation).
        """
        if not twig_results:
            return set()

        result = set()
        for twig_set in twig_results:
            result |= twig_set

        return result

    def execute_query(self, query_dict: dict, operation="AND") -> Tuple[Set[str], List[Set[str]]]:
        """
        Execute a multi-twig query across all documents.

        Args:
            query_dict: Multi-twig query
            operation: "AND" (intersection) or "OR" (union)

        Returns:
            Tuple of (final_matches, twig_results)
        """
        twig_results = self.process_query_twigs(query_dict)

        if operation == "AND":
            final_matches = self.intersect_results(twig_results)
        elif operation == "OR":
            final_matches = self.union_results(twig_results)
        else:
            raise ValueError("operation must be 'AND' or 'OR'")

        return final_matches, twig_results

    def print_results(self, query_dict: dict, final_matches: Set[str],
                     twig_results: List[Set[str]], operation: str = "AND"):
        """Pretty print query results."""
        print("=" * 70)
        print(f"Multi-Document Query (Operation: {operation})")
        print("=" * 70)
        print(f"Total Documents: {self.total_docs}\n")

        print("Query Twigs:")
        for i, (twig_key, twig_condition) in enumerate(query_dict.items(), 1):
            print(f"  Twig {i}: {twig_key}")
            print(f"    Matches: {twig_results[i-1]}")

        print(f"\n{operation} Operation Result: {final_matches}")
        print(f"Documents Matched: {len(final_matches)} / {self.total_docs}")

        print("\nDetailed Results:")
        print("-" * 70)

        if final_matches:
            for doc_id in sorted(final_matches):
                doc = self.documents[doc_id]
                company_name = doc.get("company", doc).get("name", "Unknown")
                print(f"✓ Document {doc_id}: {company_name}")
        else:
            print("No documents match the query conditions.")

        # Non-matching
        non_matching = set(self.documents.keys()) - final_matches
        if non_matching:
            print(f"\nNon-Matching Documents: {len(non_matching)}")
            for doc_id in sorted(non_matching):
                doc = self.documents[doc_id]
                company_name = doc.get("company", doc).get("name", "Unknown")
                print(f"✗ Document {doc_id}: {company_name}")


# ==================== EDGE CASE TEST SUITE ====================

class EdgeCaseTestSuite:
    """Test suite for hierarchical search edge cases."""

    def __init__(self, validator: MultiDocumentValidator):
        self.validator = validator
        self.results = []

    def test_case(self, name: str, query: dict, expected_count: int = None,
                  operation: str = "AND", description: str = ""):
        """Run a single test case."""
        print(f"\n{'=' * 70}")
        print(f"TEST: {name}")
        print(f"{'=' * 70}")
        if description:
            print(f"Description: {description}\n")

        matches, twig_results = self.validator.execute_query(query, operation)
        self.validator.print_results(query, matches, twig_results, operation)

        # Verify expectation
        success = True
        if expected_count is not None:
            if len(matches) == expected_count:
                print(f"\n✓ PASS: Found {len(matches)} matches as expected")
            else:
                print(f"\n✗ FAIL: Expected {expected_count} matches, got {len(matches)}")
                success = False

        self.results.append({
            "name": name,
            "passed": success,
            "matched": len(matches),
            "expected": expected_count
        })

        return matches, twig_results

    def run_all_tests(self):
        """Run all edge case tests."""
        print("\n\n" + "🔍 " * 20)
        print("EDGE CASE TEST SUITE - HIERARCHICAL SEARCH")
        print("🔍 " * 20)

        # Test 1: Empty query
        self.test_case(
            "Empty Query",
            {},
            0,
            description="Query with no twigs should return no matches"
        )

        # Test 2: Single twig query
        self.test_case(
            "Single Twig - Department Query",
            {"departments": {"name": "Engineering"}},
            description="Query for all documents with Engineering department"
        )

        # Test 3: Multi-level nesting
        self.test_case(
            "Multi-Level Nesting - Department with Employee Role",
            {"departments": {"name": "Engineering", "employees": {"role": "Engineer"}}},
            description="Query with multiple nesting levels - department name AND specific employee role"
        )

        # Test 4: Multiple twigs - AND operation
        self.test_case(
            "Multiple Twigs - AND Operation",
            {
                "departments": {"name": "Engineering"},
                "locations": {"country": "USA"}
            },
            operation="AND",
            description="Documents must have BOTH Engineering dept AND USA location"
        )

        # Test 5: Multiple twigs - OR operation
        self.test_case(
            "Multiple Twigs - OR Operation",
            {
                "departments": {"name": "Engineering"},
                "departments": {"name": "Sales"}
            },
            operation="OR",
            description="Documents with EITHER Engineering OR Sales (simulated with same key)"
        )

        # Test 6: Non-existent field
        self.test_case(
            "Non-Existent Field Query",
            {"nonexistent_field": {"value": "test"}},
            0,
            description="Query for non-existent field should return no matches"
        )

        # Test 7: Array matching
        self.test_case(
            "Array Matching - Multiple Locations",
            {"locations": {"city": "New York"}},
            description="Search within array of locations"
        )

        # Test 8: Deep nesting with multiple conditions
        self.test_case(
            "Deep Nesting - Complex Query",
            {
                "departments": {
                    "name": "Engineering",
                    "employees": {
                        "role": "Manager",
                        "salary": 150000
                    }
                }
            },
            description="Query with multiple conditions in nested structure"
        )

        # Test 9: Exact match
        self.test_case(
            "Exact String Match",
            {"locations": {"country": "USA"}},
            description="Exact string matching in location query"
        )

        # Test 10: Case sensitivity
        self.test_case(
            "Case Sensitivity Check",
            {"locations": {"country": "usa"}},  # lowercase
            0,
            description="Verify that search is case-sensitive"
        )

        # Print summary
        self._print_summary()

    def _print_summary(self):
        """Print test summary."""
        print("\n\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)

        passed = sum(1 for r in self.results if r["passed"])
        failed = sum(1 for r in self.results if not r["passed"])

        for result in self.results:
            status = "✓ PASS" if result["passed"] else "✗ FAIL"
            print(f"{status}: {result['name']} (matched: {result['matched']}, expected: {result['expected']})")

        print(f"\nTotal: {len(self.results)} tests, {passed} passed, {failed} failed")
        print("=" * 70)


# ==================== MAIN EXECUTION ====================

if __name__ == "__main__":
    # Generate dataset
    print("Generating dynamic company dataset...")
    gen = CompanyDataGenerator(seed=42)
    documents = gen.generate_dataset_with_specific_data(n_companies=5)

    # Initialize validator
    validator = MultiDocumentValidator(documents)

    # Run edge case tests
    test_suite = EdgeCaseTestSuite(validator)
    test_suite.run_all_tests()

    print("\n\nExample Custom Query:")
    print("=" * 70)
    matches, twig_results = validator.execute_query({
        "departments": {"name": "Engineering"},
        "locations": {"country": "USA"}
    })
    validator.print_results(
        {"departments": {"name": "Engineering"}, "locations": {"country": "USA"}},
        matches,
        twig_results
    )


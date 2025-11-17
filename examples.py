import json
from multi_doc_validator import MultiDocumentValidator
from data_generator import CompanyDataGenerator


def load_generated_companies():
    """Load companies from generated_companies.json"""
    try:
        with open("generated_companies.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: generated_companies.json not found. Generating new dataset...")
        gen = CompanyDataGenerator(seed=42)
        documents = gen.generate_dataset_with_specific_data(n_companies=5)
        return documents


def print_section(title):
    print(f"\n{'=' * 80}")
    print(f"  {title}")
    print(f"{'=' * 80}\n")


def example_1_basic_single_twig(documents):
    print_section("EXAMPLE 1: Basic Single Twig Query")

    validator = MultiDocumentValidator(documents)

    print("Find all companies with Engineering department:\n")

    query = {
        "departments": {"name": "Engineering"}
    }

    print(f"Query: {query}\n")
    matches, twig_results = validator.execute_query(query)
    validator.print_results(query, matches, twig_results)


def example_2_multi_twig_and(documents):
    print_section("EXAMPLE 2: Multi-Twig Query (AND Operation)")

    validator = MultiDocumentValidator(documents)

    print("Find companies with BOTH Engineering department AND USA location:\n")

    query = {
        "departments": {"name": "Engineering"},
        "locations": {"country": "USA"}
    }

    print(f"Query: {query}\n")
    matches, twig_results = validator.execute_query(query, operation="AND")
    validator.print_results(query, matches, twig_results, operation="AND")


def example_3_multi_twig_or(documents):
    print_section("EXAMPLE 3: Multi-Twig Query (OR Operation)")

    validator = MultiDocumentValidator(documents)

    print("Find companies with EITHER Marketing OR Sales department:\n")

    query = {
        "departments": {"name": "Engineering"}
    }

    print("Note: For true OR with different department names, process separately:\n")

    matches1, _ = validator.execute_query({"departments": {"name": "Marketing"}})
    matches2, _ = validator.execute_query({"departments": {"name": "Sales"}})

    print(f"Companies with Marketing: {matches1}")
    print(f"Companies with Sales: {matches2}")

    combined = matches1 | matches2  # Union
    print(f"\nCompanies with Marketing OR Sales: {combined}")


def example_4_nested_query(documents):
    print_section("EXAMPLE 4: Deeply Nested Query")

    validator = MultiDocumentValidator(documents)

    print("Find companies with Engineering department containing specific employees:\n")

    query = {
        "departments": {
            "name": "Engineering",
            "employees": {"role": "Engineer"}
        }
    }

    print(f"Query: {query}\n")
    matches, twig_results = validator.execute_query(query)
    validator.print_results(query, matches, twig_results)


def example_5_three_twig_complex(documents):
    print_section("EXAMPLE 5: Complex Query with Multiple Twigs")

    validator = MultiDocumentValidator(documents)

    print("Find companies that have:\n")
    print("  1. Engineering OR Sales departments")
    print("  2. USA location")
    print("  3. Employees with Manager role\n")

    query_dept = {"departments": {"name": "Engineering"}}
    query_loc = {"locations": {"country": "USA"}}
    query_emp = {"departments": {"employees": {"role": "Manager"}}}

    matches1, _ = validator.execute_query(query_dept)
    matches2, _ = validator.execute_query(query_loc)
    matches3, _ = validator.execute_query(query_emp)

    print(f"Engineering departments: {matches1}")
    print(f"USA locations: {matches2}")
    print(f"With Manager employees: {matches3}")

    final = matches1 & matches2 & matches3
    print(f"\nAll three conditions (AND): {final}\n")

    for doc_id in sorted(final):
        doc = documents[doc_id]
        print(f"✓ {doc_id}: {doc['company']['name']}")

    if not final:
        print("No companies match all three conditions")


def example_6_large_dataset(documents):
    print_section("EXAMPLE 6: Querying Large Dataset (5 companies)")

    validator = MultiDocumentValidator(documents)

    print(f"Using {len(documents)} companies from generated_companies.json\n")

    query = {
        "departments": {"name": "Engineering"},
        "locations": {"country": "USA"}
    }

    print(f"Query: Find companies with Engineering + USA\n")
    matches, twig_results = validator.execute_query(query)

    print(f"Results:")
    print(f"  - Twig 1 (Engineering): {len(twig_results[0])} matches")
    print(f"  - Twig 2 (USA): {len(twig_results[1])} matches")
    print(f"  - Final (AND): {len(matches)} companies")
    print(f"\nMatched companies: {sorted(matches)[:10]}{'...' if len(matches) > 10 else ''}")


def example_7_dynamic_generation():
    print_section("EXAMPLE 7: Dynamic Dataset Generation")

    print("Generating diverse company structures:\n")

    gen = CompanyDataGenerator(seed=42)

    print("1. Single department, single location:")
    company1 = gen.generate_company("c1", "StartupX", num_departments=1, num_locations=1)
    print(f"   {company1['company']['name']}: {len(company1['company']['departments'])} dept(s), "
          f"{len(company1['company']['locations'])} location(s)\n")

    print("2. Many departments, many locations:")
    company2 = gen.generate_company("c2", "MegaCorp", num_departments=10, num_locations=8)
    print(f"   {company2['company']['name']}: {len(company2['company']['departments'])} dept(s), "
          f"{len(company2['company']['locations'])} location(s)\n")

    print("3. Specific employees and locations:")
    department = gen.generate_department("Finance")
    location = gen.generate_location("San Francisco", "USA")
    print(f"   Department: {department['name']} with {len(department['employees'])} employees")
    print(f"   Location: {location['city']}, {location['country']}\n")


def example_8_edge_cases(documents):
    print_section("EXAMPLE 8: Edge Cases")

    validator = MultiDocumentValidator(documents)

    edge_cases = [
        {
            "name": "Empty query",
            "query": {},
            "expected": 0
        },
        {
            "name": "Non-existent field",
            "query": {"nonexistent": {"field": "value"}},
            "expected": 0
        },
        {
            "name": "Case-sensitive mismatch",
            "query": {"locations": {"country": "usa"}},  # lowercase
            "expected": 0
        },
        {
            "name": "Valid query",
            "query": {"locations": {"country": "USA"}},
            "expected": "> 0"
        }
    ]

    for case in edge_cases:
        matches, _ = validator.execute_query(case["query"])
        result_text = f"{len(matches)} matches" if isinstance(case["expected"], int) else f"{len(matches)} matches"
        status = "✓" if (isinstance(case["expected"], int) and len(matches) == case["expected"] or
                        case["expected"] == "> 0" and len(matches) > 0) else "✗"
        print(f"{status} {case['name']}: {result_text}")


def main():
    print("\n" + "🎯" * 40)
    print("HIERARCHICAL SEARCH VALIDATOR - EXAMPLES")
    print("🎯" * 40)

    documents = load_generated_companies()
    print(f"\nLoaded {len(documents)} companies from generated_companies.json")

    examples = [
        ("1. Basic Single Twig Query", example_1_basic_single_twig),
        ("2. Multi-Twig AND Operation", example_2_multi_twig_and),
        ("3. Multi-Twig OR Operation", example_3_multi_twig_or),
        ("4. Deeply Nested Query", example_4_nested_query),
        ("5. Complex Multi-Twig Query", example_5_three_twig_complex),
        ("6. Large Dataset Query", example_6_large_dataset),
        ("7. Dynamic Data Generation", example_7_dynamic_generation),
        ("8. Edge Cases", example_8_edge_cases),
    ]

    print("\nAvailable Examples:")
    for name, _ in examples:
        print(f"  {name}")

    print("\n" + "-" * 80)

    for name, func in examples:
        try:
            if "Dynamic Data Generation" in name:
                func()
            else:
                func(documents)
        except Exception as e:
            print(f"\n✗ Error in {name}: {str(e)}")

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()


import json
import random
from typing import Dict, List, Any

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Iris", "Jack"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
COMPANY_NAMES = ["TechCorp", "SalesCo", "FinanceHub", "StartupX", "InnovateLabs", "DataSystems", "CloudNet", "SecureIO"]
WORDS = ["Project", "Initiative", "System", "Platform", "Solution", "Framework", "Service", "Engine"]

class CompanyDataGenerator:

    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
        self.departments = ["Engineering", "Marketing", "Sales", "HR", "Finance", "Operations"]
        self.roles = ["Engineer", "Manager", "Analyst", "Lead", "Coordinator", "Specialist"]
        self.project_statuses = ["ongoing", "completed", "planned", "on-hold"]
        self.countries = ["USA", "UK", "Canada", "Germany", "France", "Greece", "India", "Australia"]
        self.cities = {
            "USA": ["New York", "San Francisco", "Chicago", "Austin", "Seattle"],
            "UK": ["London", "Manchester", "Edinburgh", "Birmingham", "Bristol"],
            "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
            "Germany": ["Berlin", "Munich", "Hamburg", "Frankfurt", "Cologne"],
            "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
            "Greece": ["Athens", "Thessaloniki", "Patras", "Larissa"],
            "India": ["Bangalore", "Mumbai", "Delhi", "Pune", "Chennai"],
            "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
        }

    def generate_employee(self, name=None) -> Dict[str, Any]:
        if not name:
            name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        return {
            "name": name,
            "role": random.choice(self.roles),
            "salary": random.randint(50000, 200000),
            "experience_years": random.randint(1, 20)
        }

    def generate_project(self) -> Dict[str, Any]:
        return {
            "title": f"{random.choice(WORDS)} {random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon'])}",
            "status": random.choice(self.project_statuses),
            "budget": random.randint(10000, 500000),
            "team_size": random.randint(3, 50)
        }

    def generate_department(self, dept_name=None) -> Dict[str, Any]:
        return {
            "name": dept_name or random.choice(self.departments),
            "budget": random.randint(100000, 5000000),
            "employees": [self.generate_employee() for _ in range(random.randint(2, 8))],
            "projects": [self.generate_project() for _ in range(random.randint(1, 5))]
        }

    def generate_location(self, city=None, country=None) -> Dict[str, Any]:
        country = country or random.choice(self.countries)
        city = city or random.choice(self.cities[country])
        return {
            "city": city,
            "country": country,
            "office_size": random.choice(["small", "medium", "large"]),
            "employees_count": random.randint(10, 500)
        }

    def generate_company(self, company_id: str, name: str = None,
                        num_departments: int = None,
                        num_locations: int = None) -> Dict[str, Any]:
        num_departments = num_departments or random.randint(2, 5)
        num_locations = num_locations or random.randint(1, 4)

        if not name:
            name = random.choice(COMPANY_NAMES)

        return {
            "company": {
                "id": company_id,
                "name": name,
                "founded_year": random.randint(1990, 2023),
                "industry": random.choice(WORDS),
                "revenue": random.randint(1000000, 1000000000),
                "departments": [self.generate_department() for _ in range(num_departments)],
                "locations": [self.generate_location() for _ in range(num_locations)]
            }
        }

    def generate_dataset(self, n_companies: int = 5) -> Dict[str, Dict[str, Any]]:
        dataset = {}
        for i in range(1, n_companies + 1):
            dataset[str(i)] = self.generate_company(f"c{i}")
        return dataset

    def generate_dataset_with_specific_data(self, n_companies: int = 5) -> Dict[str, Dict[str, Any]]:
        dataset = {}

        dataset["1"] = self.generate_company("c1", "TechCorp")
        dataset["1"]["company"]["departments"] = [
            self.generate_department("Engineering"),
            self.generate_department("Marketing")
        ]
        dataset["1"]["company"]["locations"] = [
            self.generate_location("New York", "USA"),
            self.generate_location("London", "UK")
        ]

        dataset["2"] = self.generate_company("c2", "SalesCo")
        dataset["2"]["company"]["departments"] = [
            self.generate_department("Sales"),
            self.generate_department("HR")
        ]
        dataset["2"]["company"]["locations"] = [
            self.generate_location("Austin", "USA"),
            self.generate_location("Berlin", "Germany")
        ]

        dataset["3"] = self.generate_company("c3", "FinanceHub")
        dataset["3"]["company"]["departments"] = [
            self.generate_department("Finance"),
            self.generate_department("Operations")
        ]
        dataset["3"]["company"]["locations"] = [
            self.generate_location("Paris", "France"),
            self.generate_location("Berlin", "Germany"),
            self.generate_location("Amsterdam", "Netherlands") if "Netherlands" in self.cities else self.generate_location("Zurich", "Switzerland")
        ]

        dataset["4"] = self.generate_company("c4", "StartupX")
        dataset["4"]["company"]["departments"] = [self.generate_department("Engineering")]
        dataset["4"]["company"]["locations"] = [self.generate_location("San Francisco", "USA")]

        for i in range(5, n_companies + 1):
            dataset[str(i)] = self.generate_company(f"c{i}")

        return dataset


if __name__ == "__main__":
    gen = CompanyDataGenerator(seed=42)

    dataset = gen.generate_dataset_with_specific_data(5)

    print("Generated Dataset Summary:")
    print("=" * 60)
    for cid, company_data in dataset.items():
        company = company_data["company"]
        print(f"\n{cid}: {company['name']}")
        print(f"  Departments: {[d['name'] for d in company['departments']]}")
        locations = [f"{l['city']}, {l['country']}" for l in company['locations']]
        print(f"  Locations: {locations}")

    with open("generated_companies.json", "w") as f:
        json.dump(dataset, f, indent=2)
    print("\n\nDataset saved to generated_companies.json")


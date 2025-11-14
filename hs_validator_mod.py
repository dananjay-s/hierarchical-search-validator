import json
from typing import Any, List

company_json = {
    "1": json.loads("""{
        "company": {
            "id": "c1",
            "name": "TechCorp",
            "departments": [
                {
                    "name": "Marketing",
                    "budget": 2000000,
                    "employees": [
                        {"name": "Alice", "role": "Engineer"},
                        {"name": "Bob", "role": "Manager"}
                    ],
                    "projects": [
                        {"title": "Project X", "status": "ongoing"},
                        {"title": "Project Y", "status": "completed"}
                    ]
                },
                {
                    "name": "Sales",
                    "budget": 300000,
                    "employees": [
                        {"name": "Alice", "role": "Salesperson"},
                        {"name": "Mallory", "role": "Manager"}
                    ],
                    "projects": [
                        {"title": "Project A", "status": "completed"},
                        {"title": "Project B", "status": "ongoing"}
                    ]
                }
            ],
            "locations": [
                {"city": "Athens", "country": "USA"},
                {"city": "Berlin", "country": "Greece"}
            ]
        }
    }"""),
    "2": json.loads("""{
        "company": {
            "id": "c2",
            "name": "BizInc",
            "departments": [
                {
                    "name": "Marketing",
                    "budget": 800000,
                    "employees": [
                        {"name": "Eve", "role": "Marketer"},
                        {"name": "David", "role": "Manager"}
                    ],
                    "projects": [
                        {"title": "Project Z", "status": "ongoing"},
                        {"title": "Project W", "status": "planned"}
                    ]
                },
                {
                    "name": "Engineering",
                    "budget": 800000,
                    "employees": [
                        {"name": "Frank", "role": "Manager"},
                        {"name": "Bob", "role": "Engineer"},
                        {"name": "Alice", "role": "Engineer"}
                    ],
                    "projects": [
                        {"title": "Project Alpha", "status": "completed"},
                        {"title": "Project Beta", "status": "ongoing"}
                    ]
                }
            ],
            "locations": [
                {"city": "Athens", "country": "USA"},
                {"city": "London", "country": "UK"}
            ]
        }
    }""")
}

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

query_tree = QueryNode("departments", {
    "name": "Marketing",
    "employees": {"name": "Bob"}
})

for cid, obj in company_json.items():
    data_tree = Node("company", obj["company"])
    if match_subtree(data_tree, query_tree):
        print(f"Company {obj['company']['name']} matches query.")
    else:
        print(f"Company {obj['company']['name']} does NOT match.")

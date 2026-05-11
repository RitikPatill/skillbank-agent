"""Tests for SkillBank (M2)."""

import uuid

import pytest
from skillbank.skill_bank import Skill, SkillBank


@pytest.fixture
def bank():
    # Unique collection name prevents EphemeralClient shared-memory leakage
    return SkillBank(persist_directory=None, collection_name=uuid.uuid4().hex)


def test_add_and_list(bank):
    skill = Skill(
        name="reverse_string",
        description="Reverse a string",
        code="def reverse_string(s): return s[::-1]",
        tags=["string", "utility"],
    )
    added = bank.add_skill(skill)
    assert added is True
    skills = bank.list_skills()
    assert len(skills) == 1
    assert skills[0].name == "reverse_string"
    assert skills[0].code == "def reverse_string(s): return s[::-1]"
    assert "string" in skills[0].tags


def test_round_trip_fields(bank):
    skill = Skill(
        name="add_numbers",
        description="Add two numbers together",
        code="def add(a, b): return a + b",
        tags=["math", "arithmetic"],
    )
    bank.add_skill(skill)
    skills = bank.list_skills()
    assert len(skills) == 1
    result = skills[0]
    assert result.id == skill.id
    assert result.name == skill.name
    assert result.description == skill.description
    assert result.code == skill.code
    assert result.tags == skill.tags


def test_search_returns_relevant(bank):
    bank.add_skill(Skill(
        name="sum_numbers",
        description="Sum two integer numbers",
        code="def add(a, b): return a + b",
        tags=["math"],
    ))
    bank.add_skill(Skill(
        name="reverse_string",
        description="Reverse a string character by character",
        code="def reverse_string(s): return s[::-1]",
        tags=["string"],
    ))
    results = bank.search_skills("sum two numbers", top_k=1)
    assert len(results) == 1
    assert results[0].name == "sum_numbers"


def test_search_top_k_respected(bank):
    descriptions = [
        ("skill_a", "Sort a list of integers"),
        ("skill_b", "Find the maximum value in a list"),
        ("skill_c", "Compute the average of a list"),
        ("skill_d", "Filter even numbers from a list"),
    ]
    for name, desc in descriptions:
        bank.add_skill(Skill(name=name, description=desc, code=f"# {name}", tags=[]))
    results = bank.search_skills("list operations", top_k=2)
    assert len(results) == 2


def test_dedup_blocks_near_duplicate(bank):
    desc = "Reverse a string character by character"
    bank.add_skill(Skill(name="reverse_string", description=desc, code="code1", tags=[]))
    result = bank.add_skill(Skill(name="reverse_string_v2", description=desc, code="code2", tags=[]))
    assert result is False
    assert len(bank.list_skills()) == 1


def test_dedup_allows_distinct(bank):
    bank.add_skill(Skill(
        name="sort_list",
        description="Sort a list of integers in ascending order",
        code="sorted(lst)",
        tags=["list"],
    ))
    bank.add_skill(Skill(
        name="read_file",
        description="Read the contents of a text file from disk",
        code="open(path).read()",
        tags=["io"],
    ))
    assert len(bank.list_skills()) == 2


def test_reset_clears_all(bank):
    bank.add_skill(Skill(name="skill_a", description="Compute square root of a number", code="import math; math.sqrt(x)", tags=["math"]))
    bank.add_skill(Skill(name="skill_b", description="Sort a list of integers in ascending order", code="sorted(lst)", tags=["list"]))
    assert len(bank.list_skills()) == 2
    bank.reset()
    assert bank.list_skills() == []


def test_search_empty_bank(bank):
    results = bank.search_skills("anything")
    assert results == []

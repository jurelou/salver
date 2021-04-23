from salver.config import api_config
from salver.common.database import DatabaseManager
from salver.common import models
from salver.common.database import exceptions
import pytest
import uuid

db_manager = DatabaseManager(
    neo4j_config=api_config.neo4j,
    elasticsearch_config=api_config.elasticsearch,
    mongodb_config=api_config.mongodb,
)

def test_duplicate_case():
    case_name = "test-duplicate-case"
    case1 = models.Case(name=case_name)
    case_id = db_manager.add_case(case1)

    case_in_db = db_manager.get_case(case_id)
    assert case_in_db.name == case_name

    case2 = models.Case(name=case_name)
    with pytest.raises(exceptions.CaseAlreadyExists):
        case_id = db_manager.add_case(case2)

def test_scan_not_found():
    with pytest.raises(exceptions.ScanNotFound):
        db_manager.get_scan(42)

def test_case_not_found():
    with pytest.raises(exceptions.CaseNotFound):
        db_manager.get_case(42)

from main.logic.usecases.claim_payday.claim_payday import ClaimPaydayUseCase
from test.db.db_config_test import connect
from test.db.db_config_test import prepare_tables
from test.db.db_config_test import drop_tables


def test_claim_payday_returns_response_with_payday_claimed_succesfully():
    drop_tables()
    prepare_tables()
    result = ClaimPaydayUseCase("username", "author").execute(connect())
    assert result.message == "payday_claimed_succesfully"

from jsonschema import validate
import random
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''

@pytest.fixture
def create_order():
    """Fixture to create a new pet and place an order, returning the order ID."""
    # Use a random ID to ensure uniqueness across parameterized runs
    pet_id = random.randint(10000, 99999)
    new_pet = {
        "id": pet_id,
        "name": "testpet",
        "type": "cat",
        "status": "available"
    }
    api_helpers.post_api_data("/pets/", new_pet)

    # Place an order for the new pet
    order_data = {
        "pet_id": pet_id
    }
    order_response = api_helpers.post_api_data("/store/order", order_data)
    assert order_response.status_code == 201

    order_id = order_response.json()["id"]
    return order_id


@pytest.mark.parametrize("new_status", ["sold", "available"])
def test_patch_order_by_id(create_order, new_status):
    order_id = create_order
    patch_endpoint = f"/store/order/{order_id}"
    patch_data = {
        "status": new_status
    }

    response = api_helpers.patch_api_data(patch_endpoint, patch_data)

    # Validate the response code is 200
    assert response.status_code == 200

    # Validate the response message
    assert_that(response.json()["message"], is_("Order and pet status updated successfully"))

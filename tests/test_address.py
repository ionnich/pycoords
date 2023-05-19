from pycoords.address import address_from_string

t_address = (
    "Maddison Square Garden, 123 Main St, Anytown, CA, 12345, USA, 38.1234, -121.1234"
)


def test_address_from_string():
    address = address_from_string(t_address)
    assert address.name == "Maddison Square Garden"
    assert address.address == "123 Main St"
    assert address.city == "Anytown"
    assert address.state_code == "CA"
    assert address.postal_code == "12345"
    assert address.country_code == "USA"
    assert address.latitude == "38.1234"
    assert address.longitude == "-121.1234"


def test_creates_separate_instances():
    address1 = address_from_string(t_address)
    address2 = address_from_string(t_address)
    assert address1 is not address2


def test_incomplete_address():
    # remove last two fields from t_address
    t_address_incomplete = ",".join(t_address.split(",")[:-2])

    address = address_from_string(t_address_incomplete)
    assert address.name == "Maddison Square Garden"
    assert address.address == "123 Main St"
    assert address.city == "Anytown"
    assert address.state_code == "CA"
    assert address.postal_code == "12345"
    assert address.country_code == "USA"
    assert address.latitude is None
    assert address.longitude is None


def test_empty_address():
    address = address_from_string("".strip())
    assert address.name is None
    assert address.address is None
    assert address.city is None
    assert address.state_code is None
    assert address.postal_code is None
    assert address.country_code is None
    assert address.latitude is None
    assert address.longitude is None

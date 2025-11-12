def test_basic():
    assert 1 + 1 == 2


def test_import_and_context_manager():
    from rapps_sdk import Client
    from rapps_sdk.auth import ApiKey
    c = Client("https://api.example.com", ApiKey("demo-key"))
    c.close()

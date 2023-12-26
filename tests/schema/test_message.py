def test_message_schema(example_message, example_message_components):
    assert example_message_components == example_message.__async_api_components__.as_schema()

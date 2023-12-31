from message_flow import Channel, MessageFlow
from message_flow.app._simple_messaging import SimpleMessageConsumer


def test_dispatch__dry_run():
    app = MessageFlow(message_consumer=SimpleMessageConsumer(dry_run=True))

    app.dispatch()

    assert app._message_consumer.closed
    assert app._message_producer.closed


def test_dispatch__error():
    app = MessageFlow(message_consumer=SimpleMessageConsumer(throw_error=True))

    app.dispatch()

    assert app._message_consumer.closed
    assert app._message_producer.closed


def test__find_or_create_channel__channel_already_added():
    test_address = "test_address"

    channel = Channel(test_address)
    app = MessageFlow(channels=[channel], message_consumer=SimpleMessageConsumer(throw_error=True))

    assert channel == app._find_or_create_channel(test_address)

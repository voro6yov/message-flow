from message_flow import Message

from .message_flow_unit_test_support import MessageFlowUnitTestSupport


def test_publishing__successful(
    test_channel: str,
    test_message: type[Message],
    test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .publisher()
                .with_channel(test_channel)
                .for_event(test_message)
        .expect()
            .publish(test_message_object)
        .expect_successful_send(test_message_object, test_channel)
    )
    # fmt: on


def test_publishing__without_channel__successful(
    test_channel: str,
    test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .publisher()
        .expect()
            .publish(test_message_object, test_channel)
        .expect_successful_send(test_message_object, test_channel)
    )
    # fmt: on


def test_publishing__without_channel__error(
    test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .publisher()
        .expect()
            .publish(test_message_object)
        .expect_error(RuntimeError)
    )
    # fmt: on


def test_publishing__channel_not_found(
    test_channel: str,
    test_message: type[Message],
    another_test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .publisher()
                .with_channel(test_channel)
                .for_event(test_message)
        .expect()
            .publish(another_test_message_object)
        .expect_error(RuntimeError)
    )
    # fmt: on

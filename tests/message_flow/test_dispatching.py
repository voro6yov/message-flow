from message_flow import Message

from .message_flow_unit_test_support import MessageFlowUnitTestSupport


def test_dispatching__successful(
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
        .and_given()
            .dispatcher()
                .subscribed_to(test_channel)
                .with_event(test_message)
        .expect()
            .dispatch()
        .expect_successful_consume()
    )
    # fmt: on


def test_dispatching__no_subscription(
    test_channel: str,
    test_message: type[Message],
    another_test_message: type[Message],
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
        .and_given()
            .dispatcher()
                .subscribed_to(test_channel)
                .with_event(another_test_message)
        .expect()
            .dispatch()
        .expect_no_consume()
    )
    # fmt: on

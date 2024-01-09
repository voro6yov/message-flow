import pytest

from message_flow import Message

from .message_flow_unit_test_support import MessageFlowUnitTestSupport


def test_sending__successful(
    test_channel: str,
    another_test_channel: str,
    test_message: type[Message],
    test_message_object: Message,
    another_test_message: type[Message],
    another_test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .sender()
                .with_channel(test_channel)
                .for_command(test_message, another_test_message, another_test_channel)
        .expect()
            .send(test_message_object)
        .expect_successful_send(test_message_object, test_channel)
        .and_given()
            .dispatcher()
                .subscribed_to(test_channel)
                .with_command(test_message, another_test_message_object)
        .expect()
            .dispatch()
        .expect_successful_consume()
        .expect_successful_send(another_test_message_object, another_test_channel)
            .dispatch_reply()
        .expect_successful_reply_consume()
    )
    # fmt: on


def test_sending__error(
    test_channel: str,
    another_test_channel: str,
    test_message: type[Message],
    another_test_message: type[Message],
    another_test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .sender()
                .with_channel(test_channel)
                .for_command(test_message, another_test_message, another_test_channel)
        .expect()
            .send(another_test_message_object)
        .expect_error()
    )
    # fmt: on


def test_sending__without_reply__successful(
    test_channel: str,
    test_message: type[Message],
    test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .sender()
                .with_channel(test_channel)
                .for_command(test_message)
        .expect()
            .send(test_message_object)
        .expect_successful_send(test_message_object, test_channel)
        .and_given()
            .dispatcher()
                .subscribed_to(test_channel)
                .with_command(test_message)
        .expect()
            .dispatch()
        .expect_successful_consume()
        .expect_no_messages_was_sent()
    )
    # fmt: on


def test_sending__without_reply__error(
    test_channel: str,
    test_message: type[Message],
    another_test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .sender()
                .with_channel(test_channel)
                .for_command(test_message)
        .expect()
            .send(another_test_message_object)
        .expect_error()
    )
    # fmt: on


def test_sending__without_channel_definition__with_reply__successful(
    test_channel: str,
    another_test_channel: str,
    test_message: type[Message],
    test_message_object: Message,
    another_test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .sender()
        .expect()
            .send(test_message_object, test_channel, another_test_channel)
        .expect_successful_send(test_message_object, test_channel)
        .and_given()
            .dispatcher()
                .subscribed_to(test_channel)
                .with_command(test_message, another_test_message_object)
        .expect()
            .dispatch()
        .expect_successful_consume()
        .expect_successful_send(another_test_message_object, another_test_channel)
    )
    # fmt: on


def test_sending__without_channel_definition__without_reply__successful(
    test_channel: str,
    test_message: type[Message],
    test_message_object: Message,
):
    # fmt: off
    (
        MessageFlowUnitTestSupport.given()
            .sender()
        .expect()
            .send(test_message_object, test_channel)
        .expect_successful_send(test_message_object, test_channel)
        .and_given()
            .dispatcher()
                .subscribed_to(test_channel)
                .with_command(test_message)
        .expect()
            .dispatch()
        .expect_successful_consume()
        .expect_no_messages_was_sent()
    )
    # fmt: on


def test_sending__command_added_only_with_reply(
    test_channel: str,
    test_message: type[Message],
    another_test_message: type[Message],
):
    with pytest.raises(RuntimeError):
        # fmt: off
        (
            MessageFlowUnitTestSupport.given()
                .sender()
                    .with_channel(test_channel)
                    .for_command(test_message, another_test_message)
            .expect()
        )
        # fmt: on


def test_sending__command_added_only_with_reply_address(
    test_channel: str,
    another_test_channel: str,
    test_message: type[Message],
):
    with pytest.raises(RuntimeError):
        # fmt: off
        (
            MessageFlowUnitTestSupport.given()
                .sender()
                    .with_channel(test_channel)
                    .for_command(test_message, reply_to=another_test_channel)
            .expect()
        )
        # fmt: on

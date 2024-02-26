from models.ack import Ack
from enums.ackStatusEnum import AckStatus
import logging as log


def on_ack_handler(content, acks):
    try:
        ack = Ack(**content)
        if ack.message_id in acks:
            acks[ack.message_id] = AckStatus.SUCCESS
        else:
            raise Exception(
                f"Ack with the message id: {ack.message_id} does not exist")
    except Exception as e:
        log.error(f"{e}")

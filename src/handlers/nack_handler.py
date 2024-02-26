from models.nack import Nack
from enums.ackStatusEnum import AckStatus
from enums.timeoutStatusEnum import TimeoutStatus
import logging as log


def on_nack_handler(content: str, acks):
    try:
        ack = Nack(**content)
        if ack.message_id in acks:
            match acks[ack.message_id]:
                case AckStatus.WAITING:
                    acks[ack.message_id] = AckStatus.FAIL
                case AckStatus.FAIL | TimeoutStatus.TIMEOUT:
                    acks[ack.message_id] = AckStatus.FAIL2
                case AckStatus.FAIL2 | TimeoutStatus.TIMEOUTU3:
                    acks[ack.message_id] = AckStatus.FAIL3
        else:
            raise Exception(
                f"Nack with the message id: {ack.message_id} does not exist")
    except Exception as e:
        log.error(f"{e}")

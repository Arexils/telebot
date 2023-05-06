from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import CallbackQuery, Message, ChatType


#
#
class IsGroup(BoundFilter):
    """
        Check if chat is group
    """

    async def check(self, obj: Message | CallbackQuery, *args):
        if isinstance(obj, Message):
            return obj.chat.id < 0
        return obj.message.chat.id < 0


class IsChannel(BoundFilter):
    async def check(self, message: Message):
        if message.forward_from_chat:
            return message.forward_from_chat.type == ChatType.CHANNEL

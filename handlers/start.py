from loader import dp, Session, chats_store
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, ChatTypeFilter
from aiogram.types.chat import ChatType
from controllers.chat import ChatController


@dp.message_handler(CommandStart(), ChatTypeFilter([ChatType.GROUP]))
async def start_command_handler(message: types.Message) -> None:
    if message.chat.id in chats_store.get_chats_ids():
        await message.answer("This chat is already tracked")
        return

    async with Session() as session:
        chat_controller = ChatController(session)
        await chat_controller.create(message.chat)
        chats_store.add_chat(message.chat)
        await session.commit()
    await message.answer("Start tracking this chat")

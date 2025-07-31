import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from main import find, initialize, min_price, collect, json
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag, Url, 
)
from aiogram.methods.send_photo import SendPhoto
from aiogram.utils.text_decorations import markdown_decoration
from aiogram import html
from aiogram.enums import ParseMode
import asyncio


# logging
logging.basicConfig(level=logging.INFO)
# bot object
bot = Bot(token="tg token here", parse_mode="HTML")
# Dispatcher
dp = Dispatcher()


def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="AWP", callback_data="weap_awp"),
            types.InlineKeyboardButton(text="AK-47", callback_data="weap_ak"),
            types.InlineKeyboardButton(text="M4A4", callback_data="weap_m4a4"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def start_parsing_ques(message: types.Message, weapon_type: str):
    kb = [
        [
            types.KeyboardButton(text="Start parsing all "+weapon_type)
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Start?"
    )
    await message.answer("Parsing "+weapon_type+"?", reply_markup=keyboard)

    
@dp.message(F.text.lower() == "start parsing all awp")
async def start_parser(message: types.Message):
    await message.answer("awp parsing started, please wait...", reply_markup=types.ReplyKeyboardRemove())

    gun_id = find('awp Worm God (Minimal Wear)')[0]
    num_of_all_pages = initialize(1, gun_id)
    wp_min_price = min_price(gun_id)
    run = collect(gun_id, wp_min_price, num_of_all_pages)

    with open('result.json', 'r') as file:
        data = json.load(file)

    for index, item in enumerate(data):
       card = as_list(
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Name", str(item.get('Name'))),
            as_key_value("Price(Y)", str(item.get('Price(Y)'))),
            as_key_value("Price without stickers(Y)", str(item.get('Price without stickers(Y)'))),
            as_key_value("Stickers price(Y)", str(item.get('Stickers price'))),
            as_key_value("Profit(%)", str(item.get('Profit'))),
            as_key_value("Overprice(¥)", str(item.get('Overprice(Y)'))),
            as_key_value("Overprice(%)", str(item.get('Overprice(proc)'))+"%"),
            marker="  ",
        ),
        Url(str(item.get('Link'))),
        sep="\n\n",
        )
       
       await message.answer("Please, wait")
       await asyncio.sleep(2)
       await bot.send_photo(chat_id = message.chat.id, photo = str(item.get('pic')), caption = card.as_markdown(), parse_mode = ParseMode.MARKDOWN_V2 )
    

@dp.message(F.text.lower() == "start parsing all ak")
async def start_parser(message: types.Message):
    await message.answer("ak-47 parsing started, please wait...", reply_markup=types.ReplyKeyboardRemove())

    gun_id = find('ak-47 Elite Build (Minimal Wear)')[0]
    num_of_all_pages = initialize(1, gun_id)
    wp_min_price = min_price(gun_id)
    run = collect(gun_id, wp_min_price, num_of_all_pages)

    with open('result.json', 'r') as file:
        data = json.load(file)
        if data == None:
            await message.answer("Nothing found, oops(")
    for index, item in enumerate(data):
       card = as_list(
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Name", str(item.get('Name'))),
            as_key_value("Price(Y)", str(item.get('Price(Y)'))),
            as_key_value("Price without stickers(Y)", str(item.get('Price without stickers(Y)'))),
            as_key_value("Stickers price(Y)", str(item.get('Stickers price'))),
            as_key_value("Profit(%)", str(item.get('Profit'))),
            as_key_value("Overprice(¥)", str(item.get('Overprice(Y)'))),
            as_key_value("Overprice(%)", str(item.get('Overprice(proc)'))+"%"),
            marker="  ",
        ),
        Url(str(item.get('Link'))),
        sep="\n\n",
        )

       await message.answer("Please, wait")
       await asyncio.sleep(2)
       await bot.send_photo(chat_id = message.chat.id, photo = str(item.get('pic')), caption = card.as_markdown(), parse_mode = ParseMode.MARKDOWN_V2 )


@dp.message(F.text.lower() == "Start parsing all m4a4")
async def start_parser(message: types.Message):
    await message.answer("m4a4 parsing started, please wait...", reply_markup=types.ReplyKeyboardRemove())

    gun_id = find('m4a4 desert-strike (field-tested)')[0]
    num_of_all_pages = initialize(1, gun_id)
    wp_min_price = min_price(gun_id)
    run = collect(gun_id, wp_min_price, num_of_all_pages)

    with open('result.json', 'r') as file:
        data = json.load(file)

    for index, item in enumerate(data):
       card = as_list(
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Name", str(item.get('Name'))),
            as_key_value("Price(Y)", str(item.get('Price(Y)'))),
            as_key_value("Price without stickers(Y)", str(item.get('Price without stickers(Y)'))),
            as_key_value("Stickers price(Y)", str(item.get('Stickers price'))),
            as_key_value("Profit(%)", str(item.get('Profit'))),
            as_key_value("Overprice(¥)", str(item.get('Overprice(Y)'))),
            as_key_value("Overprice(%)", str(item.get('Overprice(proc)'))+"%"),
            marker="  ",
        ),
        Url(str(item.get('Link'))),
        sep="\n\n",
        )

       await message.answer("Please, wait")
       await asyncio.sleep(2)
       await bot.send_photo(chat_id = message.chat.id, photo = str(item.get('pic')), caption = card.as_markdown(), parse_mode = ParseMode.MARKDOWN_V2 )
    

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Choose weapon type:", reply_markup=get_keyboard())

    
@dp.callback_query(F.data.startswith("weap_"))
async def callbacks_num(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]

    if action == "awp":
        await start_parsing_ques(callback.message, action)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    elif action == "ak":
        await start_parsing_ques(callback.message, action)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    elif action == "m4a4":
        await start_parsing_ques(callback.message, action)
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    


# Polling new updates
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

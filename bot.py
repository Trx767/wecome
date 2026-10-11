import asyncio
import logging
import random
import re
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, ChatMemberUpdatedFilter, LEAVE_TRANSITION
from aiogram.types import Message, ChatPermissions, ChatMemberUpdated

# Bot Token (Render Environment Variables ထဲတွင် TOKEN ဆိုပြီး ထည့်ပေးရပါမည်)
TOKEN = os.getenv("TOKEN", "8668928237:AAEEdsgiEz8jNBwLlkTxbSXXro33568-OCg")

dp = Dispatcher()

user_warns = {}
go_enabled = {}

MEMBER_STICKER_ID = "CAACAgUAAxkBAAESBaRqyogkWfH7WfkhpxudmYbgq8xJwAACSSEAAsSgMVeyO2hUGC56Zj0E"

INSULT_MESSAGES = [
    "အပေါစားဖာသည်မ နင့်လင်လီး ပြေးမစုပ်ရလို့ ဂါနေတာလား",
    "မင်းရဲ့စိတ်ဓာတ်ကိုပြုပြင်အကျင့်ဆိုးတွေရှင်းထုတ်နောက်ကွယ်ကနေ foul ထုမကောင်ဘူးသူများအကြောင်းကိုဆတ်မဆိုနဲ့မင်းအလုပ်ကိုယ်မင်းလူပ်",
    "မင်းကိုဘယ်သူမေးလိုက်တာလည်း စောက်ဖာသည်မသား",
    "ဖာသည်သားသေချင်တာလား",
    "ဘယ်လိုအထင်နဲ့မင်းကိုယ်မင်းဆိုလ်ရှယ်ဂေါ့လို့ထင်တာလည်းငါ့အမြင်မှာသေးသေးလေးမင်းကကျွန်ပိန်းခြေမစုပ်ပါလားရောယောင်နေတာငပိန်းလိပ်လိုးမသားနှေးလိုက်တာမြန်ရေးပြီးကို",
    "ပေးမဖားဘူးနော် မအေလိုး အခြောက်မ နာနာ ကိုက်ပြ ကြွက်မသား",
    "ဆက်ရိုက်လေ",
    "ရိုက်လေဟ",
    "ဖာသယ်မသား",
    "မင်းအမေဖာတန်းမှာဆို ငါလိုးမကုလားမင်းအမေသေဘီဆို နွားမသား",
    "အိမ်‌ေမြာင်လိုးမသား",
    "မအေလိုးကလဲနဲနဲပဲစရသေးတယ်လောင်နေဘီ",
    "ဖာသည်မသားမင်းအမေသေလို့အူမြူးနေတာလား",
    "အမ်းဟုတ်တယ်လေ ငါနိုင်တယ်",
    "မင်းအမေစပတ်ကိုမော်တာတပ်လိုးပြီးစပိုက်တာမန်းလိုကြိုးဆွဲလိုးမှာငါလိုးမဖာသယ်မဖားအိုမဖာပျက်မခွေးမနွားမသား",
    "လိပ်နဲ့တက်လိုးလို့ထွက်လာတဲ့ကောင်ကြနေတာဘဲ",
    "ညီလိုင်းမကောင်းဘူးလား ဘာလဲ ဆင်းရဲလို့လား",
    "မင်းအမေဖင်ခံတာကျွမ်းတယ်",
    "အပြောကောင်းတယ်ဖင်ခံပလား",
    "ချေပနိုင်စွမ်းမရှိ",
    "မင်းကိုကောင်းချီးပေးပြီးဖင်လိုးမှာလေစောက်ကုလား",
    "မင်းရုပ်ကမဒိန်းကောင်ရုပ်နဲ့ အနူတောမှာပဲလူချောလုပ်ရမယ်ခွေးမသားရွှာနေပြီရောဖြေနေတာလား",
    "ငါလိုးမစောက်တောသား",
    "မင်းအမေဖာသည်မအေကိုက်လို့ဝလုးချီးသုတ်ရမ်းတာလား",
    "ငါကလမ်းမတော်မှာဆျာလေမင်းကတော့ခွေးသာပေါ့",
    "တယ်လီဂရမ်မှာငါအမြန်ဆုံးကွသိဖို့",
    "ဟိတ်ခွေးမင်းငါ‌ဆဲသလိုပြန်ဆဲတာလား",
    "ခွေးရူးပြန်နေတာလား ကာကွယ်ဆေးထိုးပေးကမလားမင်းကို",
    "ဆရာခေါ်",
    "ငါလိုးမခွေးဆဲရင်ငြိမ်ခံခုန်မကိုက်နဲ့",
    "ခွေးမသားကလဲငိုဖြဲဖြဲဖြစ်နေဘီဟ",
    "ငါလိုးမသား မင်းစာဘာအဓိပ္ပာယ်မှကိုမရှိဘူး စောက်ပညာမဲ့",
    "မင်းဆရာငါဆိုတာလက်ခံတာလား",
    "ဘောမတင်းနေတာလားတင်းနေရင်ဖင်ခံလိုက်",
    "ငဒူးလာရင်အကုန်ပြေးကြတာပဲ",
    "နှမလိုးလေး",
    "ယေရှူကိုးကွယ်တဲ့ကုလားဟလီးဘဲ မင်းအမေဖာသည်မအေကိုက်လို့ဝလုးချီးသုတ်ရမ်းတာလား",
    "ဟိတ်ကောင်",
    "ခွေးမသားချီူပေတဲ့လက်နဲ့ ရွေခွက်ကိုနိုက်ချင်တာလား",
    "မင်းအမေကိုမင်းဖေကလိင်မဆက်ဆံတော့မင်းအမေကသူများလိုးခိုင်းရတာဟ",
    "မင်းအမေကိုငါဆားသိပ်ပြီးလိုးလိုက်လို့ရှောသွားပြီရဖ",
    "ငါမလိုးပါ",
    "ငါလိုးမဘောမသေမယ် ငနူ မင်းမျေသတာပါဟင မုသေမယ်ဘောမကိုက်",
    "မင်းအမေဗစ်ခိုးပြီးရှုတာဆို",
    "မင်းအမေတညလွတ်လိုက်လေ ဖုန်းပြင်ခပေးမယ်လေ",
    "မင်းလိုလဒူကို ငါကဘာအကြောင်းပြချက်နဲ့မေးပေးရမာ ငါမေးတာခံချင်ရင် ငါ့ဘောလာမလေ",
    "ဟုတ်တယ်ဟကုလားမဆိုတာမင်းအမ",
    "စောက်အထာကျနည်းသင်ပေးမယ်ဖေဖေခေါ်",
    "မင်းအဖေကဂေးဆိုညီ",
    "စောက်စုန်းလားလီးစုန်းလားလီးစုပ်စုန်းလားဟ",
    "ရိုက်ဟ",
    "စောက်ဘောမ",
    "ကြမ်းခြင်တာလား ညေးက မင်းစောက်ဆင့်ကအောက်ခြေမာ ဖုံသုတ်အဝတ်နဲ့ ခြေနင်းခုံသာသာပဲရှိတယ် ကိုမေကိုလိုးကြီးရ",
    "သခင်ငဒူးကမြတ်တယ်လေ",
    "စောက်ရမ်းအာထုနေမယ့်အစားမင်းအဖေကိုmaster bateဘိတ်လုပ်ပေးလိုက်ပါလားမင်းမိဘလိုးမရဲ့",
    "ငါမြန်နေတာကိုကြည့်ပြီးထူးဆန်းနေလား တပည့်😂👌",
    "နွားမသားခိုးငိုတာလားဟ",
    "ပြေးထား",
    "စာတွေကလဲလိပ်တက်လိုးလို့ထွက်လာတဲ့ကောင်ကျနေတာပဲ",
    "မင်းအမေ ဂွေးစိ ဆိုက်ကားစမုတ်တံ စိုက်သေတာ ငါတို့မသိဘူးလေ မအေလိုးရ",
    "သောက်ကုလား သေချင်တာလား စောက်သုံးမကျဘူး မအေလိုး မင်းအမေရောသေပီးလား မင်းအဖေပါပေးတယ် သွားခေါ်သွား",
    "ကိုမေလိုးညတစ်ချို့ကောင်တွေငါနယ်မြေထဲကိုလူသစ်တွေကိုအမြဲခေါ်လာတယ်",
    "မင်းအမေဖာသည်မကြီးကိုလမ်းထိပ်မှာတွေ့ခဲ့တယ်",
    "မအေလိုးမင်းကိုဆဲတယ် မင်းမိဘနှမငါတက်လိုး",
    "ငါလိုးမသားမင်းလို stt တွေရှိလို့မြန်မာနိုင်ငံမတိုးတက်တာ",
    "မင်းစော်ဖင်ကြီးကိုက်ဆွဲပစ်မယ်",
    "ဒိုင်ဆိုဆောလိုးမသား",
    "မင်းအမေအိမ်လွှတ်လိုက်ငါလိုးမသားမင်းအမေငါ့လိင်တံကြီးကိုကြိုက်နေတာမသိဘူးလား",
    "ညီမင်းစာတွေထပ်နေတယ်ဘာလဲကြောက်လို့လား",
    "အေးဟုတ်တယ် မင်းအဖြစ်က ဆုတ်လဲ ဆူးစားလဲ ရုံးလေနစ်လေပဲ လက်မြှောက်အရှုံးပေးလိုက်တော့",
    "ဘာလဲမင်းစာမှန်အောင်ငါတက်လိုးပေးပြီးထွက်လာရင် မှန်မယ်ထင်တယ်",
    "မင်းမေလိုးဖာသည်မသား ဘိတ်မရလို့ခိုးငိုတာလားဟ Typingကြတော့လဲနှေးကွေးဖာပိန်းမသား ငါနင်းတာက ငါလိုးရင်ငြိမ်နေ",
    "မင်းအ‌မေငါတက်လိုးလို့လူဖြစ်လာတာ မအာနဲ့ခွေးမသားမေမေ့သားလားဟ မင်းကလဲ ငါဆဲလို့ငိုယိုပြီးသွားတိုင်ရတယ်တဲ့",
    "ကိုမေကိုလိုး ကြောက်ရင်ကြောက်တယ် လို့အခုကတည်းကပြော လျှော်ပေးမယ်🤞🥶",
    "စာတွေမမှန်ဘူးညီ မင်းအမေကျောင်းမထားနိုင်ဘူးလားဟ",
    "မင်းအမေကဖုန်းမှန်ကွဲနေတာမပြင်ပေးနိုင်တာဆို ပိုက်ဆံမရှိတာဆို",
    "ငါ က အမေလို မင်းကိုသနားနေမာ မဟုတ်ဘူး ဘစ်အုပ်ပြီး ဒစ်စုပ်ခိုင်းလိုက်မယ် 👌",
    "စာလုံးပေါင်းသတ်ပုံတောင်မမှန်ပဲဟောင်နေတာဟ",
    "ဖာသည်မသားပေတီပေစုတ်နဲ့ မင်းမေစပကို ပြေးယပ်ကွာ",
    "မင်အမေဗစ်ရာလေးတွေမြင်ပြီးလီးတောင်တာဆို",
    "မင်းနားမလည်နိုင်လောက်အောင် မင်းစောက်ဖြုတ်ဦးနှောက်နဲ့မတွေးနိုင်လောက်အောင် ငါ့အရေးအသားက စောက်ရမ်းအထာကျနေတာလား",
    "ငှက်လိုးမသား",
    "ငါလိုးမကုလားသေမယ်",
    "ပြေးထားပန်းခြံမှာ ချုံတိုးပြီး ကပ်တိုးလေးအကွက်ရွေနေတာလားဒီနေ့တစ်မွန်ထူးချား ရူးနည်းတစ်မျိုးလားမင်းတို့တစ်မိသားစုလုံးဧရာဝတီမြစ်ထဲရေဆင်းကူးတဲ့ကိစ္စငါတို့မသိချင်ဘူး ရဖဖာသည်မသား မင်းဖေရှမ်းကြီးလား ငပိရောင်းတာ ကိုယ်မေကိုယ်လိုး အနားမကပ်နဲ့ အပုပ်နံ့ရတယ်ငါမြေလျှိုးမိုးပျံရင်မင်းဘဝစုတ်ပျက်သက်သွားမယ်",
    "နှေးကွေးနေတာပဲစာတစ်လုံးနဲ့တစ်လုံးက",
    "ရေငုပ်တာလား",
    "ဟာဘောမ မင်းအမေမချစ်လို့လား",
    "အရိုးကိုက်"
]

def parse_time(time_str: str) -> timedelta | None:
    match = re.match(r"^(\d+)([mhdw])$", time_str.lower())
    if not match:
        return None
    val, unit = int(match.group(1)), match.group(2)
    if unit == 'm':
        return timedelta(minutes=val)
    elif unit == 'h':
        return timedelta(hours=val)
    elif unit == 'd':
        return timedelta(days=val)
    elif unit == 'w':
        return timedelta(weeks=val)
    return None

def get_target_user(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user
    return None

@dp.message(Command("go"))
async def cmd_go(message: Message):
    chat_id = message.chat.id
    try:
        member = await message.bot.get_chat_member(chat_id=chat_id, user_id=message.from_user.id)
        is_admin = member.status in ["administrator", "creator"]
    except Exception as e:
        logging.error(f"Admin check error: {e}")
        is_admin = False

    if not is_admin:
        await message.answer("မင်းမာခွင့်ပြုချက်မရှိဘူး ဖာသယ်မသား သုံးချင်ရင် ဖေဖေ ခေါ son")
        await message.answer_sticker(MEMBER_STICKER_ID)
        return

    if chat_id in go_enabled and not go_enabled[chat_id]:
        return

    await message.answer("သခင့်အလိုကျဖာသယ်မသားကိုဖင်စတင်လိုးပါတော့မယ်")
    random_insult = random.choice(INSULT_MESSAGES)
    user = message.from_user
    mention = f"[{user.full_name}](tg://user?id={user.id})"
    text = f"{mention}\n{random_insult}"
    await message.answer(text, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("ungo"))
async def cmd_ungo(message: Message):
    try:
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.answer("❌ ဤ Command ကို Group ၏ Admin သို့မဟုတ် Owner များသာ အသုံးပြုနိုင်ပါသည်။")
            return
    except Exception as e:
        logging.error(f"Admin check error: {e}")
        return

    chat_id = message.chat.id
    go_enabled[chat_id] = False
    await message.answer("ခွေးမသား အားလုံးငြိမ်းချမ်းစေ")

@dp.message(Command("rgo"))
async def cmd_rgo(message: Message):
    try:
        member = await message.bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        if member.status not in ["administrator", "creator"]:
            await message.answer("❌ ဤ Command ကို Group ၏ Admin သို့မဟုတ် Owner များသာ အသုံးပြုနိုင်ပါသည်။")
            return
    except Exception as e:
        logging.error(f"Admin check error: {e}")
        return

    chat_id = message.chat.id
    go_enabled[chat_id] = True
    await message.answer("✅ `/go` ဖြင့် စာပို့ခြင်းကို ပြန်လည် ဖွင့်လိုက်ပါပြီ။")

LINK_REGEX = r"(https?://[^\s]+|t\.me/[^\s]+|telegram\.me/[^\s]+)"

@dp.message(F.text)
async def check_links_and_commands(message: Message):
    if re.search(LINK_REGEX, message.text, re.IGNORECASE):
        user = message.from_user
        chat_id = message.chat.id
        user_id = user.id

        try:
            await message.delete()
        except Exception:
            pass

        key = (chat_id, user_id)
        current_warns = user_warns.get(key, 0) + 1
        user_warns[key] = current_warns

        mention = f"[{user.full_name}](tg://user?id={user.id})"

        if current_warns >= 3:
            try:
                await message.chat.ban(user_id=user_id)
                await message.answer(f"⚠️ {mention} သည် Link (၃) ကြိမ် ပို့သောကြောင့် Group မှ Ban လိုက်ပါပြီ။")
                user_warns.pop(key, None)
            except Exception as e:
                logging.error(f"Ban Error: {e}")
        else:
            await message.answer(f"⚠️ {mention} Link ပို့ခွင့်မရှိပါ။\nသတိပေးချက်: ({current_warns}/3) ကြိမ် ရရှိထားပါသည်။ (၃) ကြိမ်ပြည့်ပါက Ban ခံရပါမည်။")
        return

@dp.message(Command("warn"))
async def cmd_warn(message: Message):
    target = get_target_user(message)
    if not target:
        await message.answer("ကျေးဇူးပြု၍ Warn ပေးလိုသူ၏ မက်ဆေ့ချ်ကို Reply ပြန်၍ ပို့ပါ။")
        return
    
    key = (message.chat.id, target.id)
    current_warns = user_warns.get(key, 0) + 1
    user_warns[key] = current_warns

    mention = f"[{target.full_name}](tg://user?id={target.id})"

    if current_warns >= 3:
        await message.chat.ban(user_id=target.id)
        await message.answer(f"⚠️ {mention} သည် Warn (၃) ကြိမ်ပြည့်သွားသောကြောင့် Ban လိုက်ပါပြီ။")
        user_warns.pop(key, None)
    else:
        await message.answer(f"⚠️ {mention} ကို Admin မှ Warn ပေးလိုက်ပါပြီ။ ({current_warns}/3)")

@dp.message(Command("warns"))
async def cmd_warns(message: Message):
    target = get_target_user(message) or message.from_user
    key = (message.chat.id, target.id)
    count = user_warns.get(key, 0)
    await message.answer(f"👤 {target.full_name} ရရှိထားသော Warn အရေအတွက်: ({count}/3)")

@dp.message(Command("resetwarns"))
async def cmd_resetwarns(message: Message):
    target = get_target_user(message)
    if not target:
        await message.answer("ကျေးဇူးပြု၍ Warn ပြန်ဖျက်ပေးလိုသူ၏ မက်ဆေ့ချ်ကို Reply ပြန်ပါ။")
        return
    key = (message.chat.id, target.id)
    user_warns.pop(key, None)
    await message.answer(f"✅ {target.full_name} ၏ Warn များကို ပြန်လည် ဖျက်ပေးလိုက်ပါပြီ။")

@dp.message(F.new_chat_members)
async def welcome_new_member(message: Message):
    for member in message.new_chat_members:
        mention = f"[{member.full_name}](tg://user?id={member.id})"
        await message.answer(f"မင်္ဂလာပါ {mention} ရေ 👋\nGroup မှ နွေးထွေးစွာ ကြိုဆိုပါတယ်။")

@dp.chat_member(ChatMemberUpdatedFilter(member_status_changed=LEAVE_TRANSITION))
async def auto_ban_on_leave(event: ChatMemberUpdated):
    try:
        await event.bot.ban_chat_member(chat_id=event.chat.id, user_id=event.from_user.id)
    except Exception as e:
        logging.error(f"Error auto-banning on leave: {e}")

@dp.message(Command("ban"))
async def cmd_ban(message: Message):
    target = get_target_user(message)
    if target:
        await message.chat.ban(user_id=target.id)
        await message.answer(f"❌ {target.full_name} ကို Ban လိုက်ပါပြီ။")

@dp.message(Command("mute"))
async def cmd_mute(message: Message):
    target = get_target_user(message)
    if target:
        await message.chat.restrict(user_id=target.id, permissions=ChatPermissions(can_send_messages=False))
        await message.answer(f"🔇 {target.full_name} ကို Mute လိုက်ပါပြီ။")

@dp.message(Command("unmute"))
async def cmd_mute_undo(message: Message):
    target = get_target_user(message)
    if target:
        await message.chat.restrict(
            user_id=target.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"🔊 {target.full_name} ကို Unmute လုပ်ပေးလိုက်ပါပြီ။")

async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

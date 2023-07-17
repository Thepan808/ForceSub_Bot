import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
async def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = await client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (await client.get_me()).id:
          try:
            await client.get_chat_member(channel, user_id)
            await client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              await cb.message.delete()
          except UserNotParticipant:
            await client.answer_callback_query(cb.id, text="❗ Junte-se ao mencionado 'canal' e pressione o botão 'Me Desmute' botão novamente.", show_alert=True)
      else:
        await client.answer_callback_query(cb.id, text="❗ Você é silenciado por administradores por outros motivos.", show_alert=True)
    else:
      if not (await client.get_chat_member(chat_id, (await client.get_me()).id)).status == 'administrator':
        await client.send_message(chat_id, f"❗ **{cb.from_user.mention} está tentando Desmutar si mesmo, mas eu não posso unmute ele porque eu não sou um administrador neste bate-papo me adicione como administrador novamente.**\n__#Saindo deste bate-papo...__")
        await client.leave_chat(chat_id)
      else:
        await client.answer_callback_query(cb.id, text="❗ Aviso: Não clique no botão se puder digitar livremente.", show_alert=True)



@Client.on_message((filters.text | filters.media) & ~filters.private & ~filters.edited, group=1)
async def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not (await client.get_chat_member(chat_id, user_id)).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      if channel.startswith("-"):
          channel_url = await client.export_chat_invite_link(int(channel))
      else:
          channel_url = f"https://t.me/{channel}"
      try:
        await client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = await message.reply_text(
              " {} , você ainda não está inscrito no meu canal. Por favor, junte-se usando o botão abaixo e pressione o botão Desmute me para desativar o mute.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Clique aqui e se inscreva no canal", url=channel_url)
                ],
                [
                    InlineKeyboardButton("Me Desmute", callback_data="onUnMuteRequest")
                ]
            ]
        )
          )
          await client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          await sent_message.edit("❗ **Eu não sou um administrador aqui.**\n__Faça-me administrador com permissão de usuário banir e me adicione novamente.\n#Saindo deste bate-papo...__")
          await client.leave_chat(chat_id)
      except ChatAdminRequired:
        await client.send_message(chat_id, text=f"❗ **Eu não sou um administrador nesse [canal]({channel_url})**\n__Faça-me administrador no canal e adicione-me novamente.\n#Saindo deste bate-papo...__")
        await client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
async def config(client, message):
  user = await client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status == "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        await message.reply_text("❌ **Force Subscribe está desativado com sucesso.**")
      elif input_str.lower() in ('clear'):
        sent_message = await message.reply_text('**Dessilenciando todos os membros que são silenciados por mim...**')
        try:
          for chat_member in (await client.get_chat_members(message.chat.id, filter="restricted")):
            if chat_member.restricted_by.id == (await client.get_me()).id:
                await client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          await sent_message.edit('✅ **Dessilenciado todos os membros que são silenciados por mim.**')
        except ChatAdminRequired:
          await sent_message.edit('❗ **Eu não sou um administrador neste bate-papo.**\n__Eu não posso\'desmutar membros porque eu não sou um administrador neste bate-papo me fazer administrador com permissão de usuário restringir.__')
      else:
        try:
          await client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          if input_str.startswith("-"):
              channel_url = await client.export_chat_invite_link(int(input_str))
          else:
              channel_url = f"https://t.me/{input_str}"
          await message.reply_text(f"✅ **Force Subscribe está habilitado**\n__Force Subscribe está habilitado, todos os membros do grupo têm que se inscrever este [canal]({channel_url}) para enviar mensagens neste grupo.__", disable_web_page_preview=True)
        except UserNotParticipant:
          await message.reply_text(f"❗ **Não é um administrador no canal**\n__Eu não sou um administrador no [canal]({channel_url}). Adicione-me como administrador para ativar o ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          await message.reply_text(f"❗ **Nome de usuário/ID do canal inválido.**")
        except Exception as err:
          await message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            channel_url = await client.export_chat_invite_link(int(input_str))
        else:
            channel_url = f"https://t.me/{my_channel}"
        await message.reply_text(f"✅ **Force Subscribe está ativado neste bate-papo.**\n__Para isso [Canal]({channel_url})__", disable_web_page_preview=True)
      else:
        await message.reply_text("❌ **Force Subscribe está desativado neste bate-papo.**")
  else:
      await message.reply_text("❗ **Criador de grupo necessário**\n__Você tem que ser o criador do grupo para fazer isso.__")

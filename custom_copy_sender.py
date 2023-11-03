from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup
import typing


class CopySender:
    """
    Custom copy sender from Aiogram2 for Aiogram3
    Author: https://github.com/roomdie/
    """

    def __init__(self, message):
        self.message = message

    async def send_copy(
            self,
            chat_id: typing.Union[str, int],
            message_thread_id: typing.Optional[int] = None,
            disable_notification: typing.Optional[bool] = None,
            protect_content: typing.Optional[bool] = None,
            disable_web_page_preview: typing.Optional[bool] = None,
            reply_to_message_id: typing.Optional[int] = None,
            allow_sending_without_reply: typing.Optional[bool] = None,
            reply_markup: typing.Union[
                InlineKeyboardMarkup, ReplyKeyboardMarkup, None
            ] = None,
    ) -> Message:
        """
        Send copy of current message

        :param chat_id:
        :param message_thread_id:
        :param disable_notification:
        :param protect_content:
        :param disable_web_page_preview: for text messages only
        :param reply_to_message_id:
        :param allow_sending_without_reply:
        :param reply_markup:
        :return:
        """
        kwargs = {
            "chat_id": chat_id,
            "message_thread_id": message_thread_id,
            "allow_sending_without_reply": allow_sending_without_reply,
            "reply_markup": reply_markup or self.message.reply_markup,
            "parse_mode": "HTML",
            "disable_notification": disable_notification,
            "protect_content": protect_content,
            "reply_to_message_id": reply_to_message_id,
        }
        text = self.message.html_text if (self.message.text or self.message.caption) else None

        if self.message.text:
            kwargs["disable_web_page_preview"] = disable_web_page_preview
            return await self.message.bot.send_message(text=text, **kwargs)
        elif self.message.audio:
            return await self.message.bot.send_audio(
                audio=self.message.audio.file_id,
                caption=text,
                title=self.message.audio.title,
                performer=self.message.audio.performer,
                duration=self.message.audio.duration,
                **kwargs,
            )
        elif self.message.animation:
            return await self.message.bot.send_animation(
                animation=self.message.animation.file_id, caption=text, **kwargs
            )
        elif self.message.document:
            return await self.message.bot.send_document(
                document=self.message.document.file_id, caption=text, **kwargs
            )
        elif self.message.photo:
            return await self.message.bot.send_photo(
                photo=self.message.photo[-1].file_id, caption=text, **kwargs
            )
        elif self.message.sticker:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_sticker(sticker=self.message.sticker.file_id, **kwargs)
        elif self.message.video:
            return await self.message.bot.send_video(
                video=self.message.video.file_id, caption=text, **kwargs
            )
        elif self.message.video_note:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_video_note(
                video_note=self.message.video_note.file_id, **kwargs
            )
        elif self.message.voice:
            return await self.message.bot.send_voice(
                voice=self.message.voice.file_id, caption=text, **kwargs
            )
        elif self.message.contact:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_contact(
                phone_number=self.message.contact.phone_number,
                first_name=self.message.contact.first_name,
                last_name=self.message.contact.last_name,
                vcard=self.message.contact.vcard,
                **kwargs,
            )
        elif self.message.venue:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_venue(
                latitude=self.message.venue.location.latitude,
                longitude=self.message.venue.location.longitude,
                title=self.message.venue.title,
                address=self.message.venue.address,
                foursquare_id=self.message.venue.foursquare_id,
                foursquare_type=self.message.venue.foursquare_type,
                **kwargs,
            )
        elif self.message.location:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_location(
                latitude=self.message.location.latitude,
                longitude=self.message.location.longitude,
                **kwargs,
            )
        elif self.message.poll:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_poll(
                question=self.message.poll.question,
                options=[option.text for option in self.message.poll.options],
                is_anonymous=self.message.poll.is_anonymous,
                allows_multiple_answers=self.message.poll.allows_multiple_answers,
                **kwargs,
            )
        elif self.message.dice:
            kwargs.pop("parse_mode")
            return await self.message.bot.send_dice(
                emoji=self.message.dice.emoji,
                **kwargs,
            )
        else:
            raise TypeError("This type of message can't be copied.")

"""Telegram notifier module."""

# -*- coding: utf-8 -*-
from __future__ import annotations

import asyncio
from typing import List, Optional

import telegram
from telegram import Bot


class TelegramNotifier:
    """Notifier for sending Telegram messages."""

    def __init__(self, bot_token: str, chat_id: str) -> None:
        """Initializes the TelegramNotifier.

        Args:
            bot_token: The Telegram bot token.
            chat_id: The Telegram chat ID.
        """
        try:
            self.bot = Bot(token=bot_token)
            self.chat_id = chat_id
        except telegram.error.TelegramError as e:
            print(f"Error initializing Telegram bot: {e}")
            raise

    async def _send_message_async(
        self,
        message: str,
        files: Optional[List[str]] = None,
        disable_notification: bool = False,
    ) -> None:
        """Sends a message to the configured Telegram chat asynchronously.

        Args:
            message: The message to send.
            files: Optional list of file paths to send as attachments.
            disable_notification: If True, sends the message silently.
        """
        try:
            # Send text message
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                disable_notification=disable_notification,
            )

            # Send files if provided
            if files:
                for file_path in files:
                    with open(file_path, "rb") as f:
                        await self.bot.send_document(
                            chat_id=self.chat_id,
                            document=f,
                            disable_notification=disable_notification,
                        )
        except telegram.error.TelegramError as e:
            print(f"Error sending Telegram message: {e}")

    def send_message(self, message: str, files: Optional[List[str]] = None) -> None:
        """Sends a message to the configured Telegram chat.

        Args:
            message: The message to send.
            files: Optional list of file paths to send as attachments.
        """
        asyncio.run(self._send_message_async(message, files, disable_notification=True))

    def send_alert(self, message: str, files: Optional[List[str]] = None) -> None:
        """Sends an alert message to the configured Telegram chat.

        Args:
            message: The message to send.
            files: Optional list of file paths to send as attachments.
        """
        alert_message = f"'@RachelKerry' {message}"
        asyncio.run(self._send_message_async(message, files))


# Performance characteristics:
# - Depends on the network speed and Telegram API response time.
# Resource usage details:
# - Minimal memory usage.
# Threading considerations:
# - python-telegram-bot is thread-safe.
# - Using asyncio to handle asynchronous calls.

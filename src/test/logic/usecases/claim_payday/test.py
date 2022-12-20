import pytest


@pytest.mark.asyncio
async def test_command(bot, message):
    # Set up the message object with the appropriate content and author
    message.content = "!command"
    message.author = bot.user

    # Send the message and wait for a response
    await bot.process_commands(message)
    response = bot.last_response

    # Assert that the bot responded with the expected message
    assert response == "expected response"
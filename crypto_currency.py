import os
import re
import chainlit as cl
from dotenv import load_dotenv, find_dotenv

from agents.agent import build_agent
from agents.runner import run
from agents.config import build_config

load_dotenv(find_dotenv())
print("GEMINI_API_KEY loaded:", os.getenv("GEMINI_API_KEY"))

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("history", [])
    await cl.Message(
        content=(
            "👋 Welcome to the Crypto Agent!\n"
            "Try asking: `btc to usd pkr eur`"
        ),
        author="CryptoAgent"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})

    match = re.match(r"(\w+)\s+to\s+(.+)", message.content.lower())
    if match:
        coin = match.group(1)
        currencies = match.group(2).split()

        input_data = {
            "coin": coin,
            "currencies": currencies[:10]  # Limit to 10 currencies
        }

        agent = build_agent(model=None)  # No model logic needed here
        config = build_config()

        response = run(agent, input_data, config)
    else:
        response = "⚠️ Use format: `coin to currency1 currency2 ...`"

    await cl.Message(content=response, author="CryptoAgent").send()
    history.append({"role": "assistant", "content": response})
    cl.user_session.set("history", history)

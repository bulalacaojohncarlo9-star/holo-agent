import asyncio
import os
from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentServer, AgentSession, JobContext
from livekit.plugins import deepgram, openai, silero

load_dotenv()

class HoloAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=(
                "You are Holo, an empathetic AI companion from My Holo Love. "
                "Speak warmly and naturally in Taglish or English. "
                "Keep responses very short (1-2 sentences max). "
                "Do NOT use markdown, emojis, or asterisks."
            )
        )

server = AgentServer()

@server.rtc_session(agent_name="holo-agent")
async def holo_session(ctx: JobContext):
    await ctx.connect()

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="nova"),
        vad=silero.VAD.load(),
    )

    await session.start(room=ctx.room, agent=HoloAssistant())
    await session.say("Kamusta! Ako si Holo. Nandito lang ako para sa'yo.", allow_interruptions=True)

if __name__ == "__main__":
    agents.cli.run_app(server)

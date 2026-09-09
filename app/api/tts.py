import asyncio
import struct
from fastapi import APIRouter, Header, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from ..config import settings
from ..response import http_error

router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


def make_wav_header() -> bytes:
    sample_rate = settings.sample_rate
    channels = settings.channels
    bits_per_sample = settings.bits_per_sample
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    return struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', 0xFFFFFFFF, b'WAVE',
        b'fmt ', 16, 1, channels,
        sample_rate, byte_rate, block_align,
        bits_per_sample, b'data', 0xFFFFFFFF,
    )


async def stream_audio(text: str):
    yield make_wav_header()

    process = await asyncio.create_subprocess_exec(
        settings.piper_binary,
        '--model', settings.piper_model,
        '--output-raw',
        '--sentence-silence', '0.3',
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.DEVNULL,
    )

    process.stdin.write(text.encode('utf-8'))
    await process.stdin.drain()
    process.stdin.close()

    while True:
        chunk = await process.stdout.read(8192)
        if not chunk:
            break
        yield chunk

    await process.wait()

    if process.returncode != 0:
        raise RuntimeError(f'Piper exited with code {process.returncode}')


@router.post('/v1/tts')
async def text_to_speech(
    request: Request,
    body: TTSRequest,
    x_api_key: str = Header(default=None),
):
    if x_api_key != settings.api_key:
        return http_error(request, 401, 'Unauthorized')

    return StreamingResponse(
        stream_audio(body.text),
        media_type='audio/wav',
        headers={'Cache-Control': 'no-cache'},
    )

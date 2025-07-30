from datetime import datetime, timezone
import io
import pyopencl as cl
from io import BytesIO
import discord
import imageio.v3 as iio
import numpy as np

def get_default_device(prefer_gpu=True):
    for platform in cl.get_platforms():
        devices = platform.get_devices()
        # Prefer GPU
        for dev in devices:
            if prefer_gpu and dev.type == cl.device_type.GPU:
                return cl.Context([dev])
        # Fallback to any device
        if devices:
            return cl.Context([devices[0]])
    raise RuntimeError("No OpenCL devices found")

ctx = get_default_device()

async def attachment_to_image(img: discord.Attachment) -> np.ndarray:
    image_bytes = await img.read()
    image_array = iio.imread(BytesIO(image_bytes), mode="RGBA")
    return image_array

def image_to_file(img: np.ndarray) -> discord.File:
    buffer = io.BytesIO()
    iio.imwrite(buffer, img, format="png")
    buffer.seek(0)
    file = discord.File(fp=buffer, filename="image.png")
    return file

def apply_effect(effect_kernel: str, img: np.ndarray, *args) -> np.ndarray:
    height, width = img.shape[:2]
    queue = cl.CommandQueue(ctx)
    fmt = cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNSIGNED_INT8)
    img_cl = cl.Image(ctx, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
                    fmt, shape=(width, height), hostbuf=img)
    out_cl = cl.Image(ctx, cl.mem_flags.WRITE_ONLY,
                    fmt, shape=(width, height))
    prg = cl.Program(ctx, effect_kernel).build()
    prg._main(queue, (width, height), None, img_cl, out_cl, *args)
    out_np = np.empty_like(img)
    # Copy GPU result back to CPU
    origin = (0, 0, 0)
    region = (width, height, 1)
    cl.enqueue_copy(queue, out_np, out_cl, origin=origin, region=region)
    return out_np

def image_to_embed(img: np.ndarray, embed_color: discord.Color) -> tuple[discord.Embed, discord.File]:
    file = image_to_file(img)
    embed = discord.Embed(title="Output Image", color=embed_color)
    embed.set_image(url="attachment://image.png")
    embed.set_footer(text="Powered by Crimbo")
    embed.timestamp = datetime.now(timezone.utc)    
    return (embed, file)

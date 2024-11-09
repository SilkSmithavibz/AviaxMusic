import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message

from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.decorators.language import language


def testspeed(m, _):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit_text(_["server_12"])
        test.download()
        m = m.edit_text(_["server_13"])
        test.upload()
        test.results.share()
        result = test.results.dict()  # This is the dictionary with speed test results
        m = m.edit_text(_["server_14"])
    except Exception as e:
        return m.edit_text(f"<code>{e}</code>")
    return result


@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client, message: Message, _):
    # Sending initial message to the user
    m = await message.reply_text(_["server_11"])

    # Run the speedtest in a separate thread to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, _)

    # Now, we assume 'result' is a dictionary, let's safely format it into output
    if isinstance(result, dict):  # Ensure result is a dictionary
        try:
            output = _["server_15"].format(
                result["client"]["isp"],
                result["client"]["country"],
                result["server"]["name"],
                result["server"]["country"],
                result["server"]["cc"],
                result["server"]["sponsor"],
                result["server"]["latency"],
                result["ping"],
            )
            # Send a photo along with the output message
            msg = await message.reply_photo(photo=result["share"], caption=output)
        except KeyError as e:
            # Handle missing keys gracefully
            output = f"<code>Missing key: {e}</code>"
            msg = await message.reply_text(output)
        except Exception as e:
            # Catch any unexpected error and return it to the user
            msg = await message.reply_text(f"<code>{e}</code>")
    else:
        # If 'result' is not a dictionary, report an error
        msg = await message.reply_text("<code>Error: Speedtest result is not a valid dictionary.</code>")

    # Delete the initial message after processing
    await m.delete()
    

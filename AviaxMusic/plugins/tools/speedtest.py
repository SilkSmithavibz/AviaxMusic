import asyncio
import speedtest
from pyrogram import filters
from pyrogram.types import Message

from AviaxMusic import app
from AviaxMusic.misc import SUDOERS
from AviaxMusic.utils.decorators.language import language


def testspeed(m, _):
    try:
        # Initialize the Speedtest object
        test = speedtest.Speedtest()
        test.get_best_server()  # Select the best server
        m = m.edit_text(_["server_12"])
        
        # Start the download test
        test.download()
        m = m.edit_text(_["server_13"])
        
        # Start the upload test
        test.upload()
        
        # Share the result (creates an image link of the result)
        test.results.share()
        
        # Get the results as a dictionary
        result = test.results.dict()
        
        # Log the result to inspect its content
        print("Speedtest result:", result)  # This will log the result to the console for debugging
        
        # Check if the result is a dictionary
        if not isinstance(result, dict):
            raise ValueError("Speedtest result is not a valid dictionary.")
        
        m = m.edit_text(_["server_14"])  # Update the status message after completion
    except Exception as e:
        # If there is an error, send a message with the error
        return m.edit_text(f"<code>{str(e)}</code>")
    
    return result


@app.on_message(filters.command(["speedtest", "spt"]) & SUDOERS)
@language
async def speedtest_function(client, message: Message, _):
    # Send an initial message to the user
    m = await message.reply_text(_["server_11"])

    # Run the speedtest in a separate thread to avoid blocking the event loop
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m, _)

    # Check if the result is a valid dictionary
    if isinstance(result, dict):
        try:
            # Format the output with relevant data from the result dictionary
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

            # Send the result as a photo along with a caption
            msg = await message.reply_photo(photo=result["share"], caption=output)
        except KeyError as e:
            # Handle missing keys gracefully
            output = f"<code>Missing key: {e}</code>"
            msg = await message.reply_text(output)
        except Exception as e:
            # Catch any unexpected error and send it to the user
            msg = await message.reply_text(f"<code>{str(e)}</code>")
    else:
        # If the result is not a dictionary, notify the user
        msg = await message.reply_text("<code>Error: Speedtest result is not a valid dictionary.</code>")

    # Delete the initial message after processing
    await m.delete()
    

from service import Service
from MysqlBase.MysqlBase import MysqlService
import asyncio
import signal
import sys

async def main():
    try:
        print("Service initialize...")
        await Service.async_init()
    except Exception as err:
        await shutdown()
        print(f"Init service failed: {err}")

async def shutdown():
    print("Shutting down...")

    try:
        await MysqlService.close()  # Close MySQL properly
    except Exception as err:
        print(f"Error closing MySQL: {err}")

    print("Shutdown complete.")

def handle_exit_signal(sig, frame):
    """ Ensure cleanup is performed before exit """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(shutdown())
    sys.exit(0)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # Handle termination signals properly
    signal.signal(signal.SIGINT, handle_exit_signal)   # Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit_signal)  # Docker stop / Cloud Run

    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down...")
        loop.run_until_complete(shutdown())
    finally:
        print("Closing event loop...")
        loop.run_until_complete(asyncio.sleep(0.1))  # Let async cleanup finish
        loop.close()
        print("Event loop closed successfully.")

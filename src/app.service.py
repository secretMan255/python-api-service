from service import Service
import asyncio
async def main():
     try:
          print('Service initialize...')
          await Service.async_init()
     except Exception as err:
          print(f'Init service failed: {err}')


if __name__ == "__main__":
    asyncio.run(main())
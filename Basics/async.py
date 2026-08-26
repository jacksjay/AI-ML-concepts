import asyncio
import time

# async def makes this an asynchronous function
async def api_call(request_id):
    print(f"Request {request_id} started...")
    
    # await asyncio.sleep(2) simulates waiting for an AI to reply. 
    # Because it is 'await', Python goes to do other things instead of freezing!
    await asyncio.sleep(2) 
    
    print(f"Request {request_id} finished!")
    return f"Response {request_id}"

async def main():
    start_time = time.time()
    
    # run 3 calls at the same time
    # asyncio.gather runs them concurrently
    tasks = [
        api_call(1),
        api_call(2),
        api_call(3)
    ]
    
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    
    print("\nAll Results:", results)
    # this takes ~2 seconds, not 6 seconds!
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

# use asyncio.run() to start an async program
asyncio.run(main())
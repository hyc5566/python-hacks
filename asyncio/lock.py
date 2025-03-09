"""
The usage of asyncio.Lock

Once a coroutine acquires the `lock`, other coroutines will be blocked until the lock is released.

"""
import asyncio

async def worker(lock):
    print("Waiting for the lock")
    async with lock:
        print("Lock acquired")
        await asyncio.sleep(2)
        print("Lock released")

async def main():
    lock = asyncio.Lock()
    await asyncio.gather(worker(lock), worker(lock), worker(lock))

if __name__ == "__main__":
    asyncio.run(main())

# Output:
# Waiting for the lock    # Worker 1 嘗試獲取鎖
# Lock acquired           # Worker 1 成功獲取鎖
# Waiting for the lock    # Worker 2 嘗試獲取鎖（但必須等待）
# Waiting for the lock    # Worker 3 嘗試獲取鎖（但必須等待）
# Lock released           # Worker 1 完成後釋放鎖
# Lock acquired           # Worker 2 獲取鎖
# Lock released           # Worker 2 完成後釋放鎖
# Lock acquired           # Worker 3 獲取鎖
# Lock released           # Worker 3 完成後釋放鎖

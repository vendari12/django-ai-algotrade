#!/usr/bin/env python3
import asyncio
import re
import time
from aiohttp import request
from aiomultiprocess import Pool
from functools import partial

TITLE_REGEXP = re.compile(r'<title>(.*)</title>')
IDXS = range(20)
URL = 'http://example.com'
URLS = [URL] * 200
TO_BE_FIBONACCIED = range(30000)


async def get(url):
    async with request('GET', url) as response:
        return await response.text('latin1')


async def get_with_index(url, idx):
    async with request('GET', url) as response:
        return (await response.text('latin1'), idx)


async def fibonacci(n):
    a = 0
    b = 1
    sum = 0
    count = 1
    while count <= n:
        count += 1
        a = b
        b = sum
        sum = a + b
    return sum


PARTIAL_GET = partial(get_with_index, URL)


async def aiomultiprocess_test_with_work():
    print('''
===========================aiomultiprocess======================================
''')
    async with Pool() as pool:
        async for result, idx in pool.map(PARTIAL_GET, IDXS):
            # Do some work on the result and display it
            print(re.findall(TITLE_REGEXP, result)[0], idx)
    print('''
================================================================================
''')


async def asyncio_test_with_work():
    print('''
===========================asyncio==============================================
''')
    tasks = [asyncio.create_task(PARTIAL_GET(idx)) for idx in IDXS]
    for task in asyncio.as_completed(tasks):
        result, idx = await task
        # Do some work on the result and display it
        print(re.findall(TITLE_REGEXP, result)[0], idx)
    print('''
================================================================================
''')


async def aiomultiprocess_test_just_requests():
    print('''
===========================aiomultiprocess======================================
''')
    async with Pool() as pool:
        # Just execute the requests
        await pool.map(get, URLS)
    print('done!')
    print('''
================================================================================
''')


async def asyncio_test_just_requests():
    print('''
===========================asyncio==============================================
''')
    tasks = [asyncio.create_task(get(url)) for url in URLS]
    await asyncio.gather(*tasks)
    print('done!')
    print('''
================================================================================
''')


async def aiomultiprocess_test_cpu_bound_work():
    print('''
===========================aiomultiprocess======================================
''')
    async with Pool() as pool:
        # Just execute the requests
        results = await pool.map(fibonacci, TO_BE_FIBONACCIED)
    print('done!')
    print('''
================================================================================
''')


async def asyncio_test_cpu_bound_work():
    print('''
===========================asyncio==============================================
''')
    tasks = [asyncio.create_task(fibonacci(n)) for n in TO_BE_FIBONACCIED]
    results = await asyncio.gather(*tasks)
    print('done!')
    print('''
================================================================================
''')


if __name__ == '__main__':
    #start_multi_work = time.time()
    #asyncio.run(aiomultiprocess_test_with_work())
    #end_multi_work = time.time()

    #start_asyncio_work = time.time()
    #asyncio.run(asyncio_test_with_work())
    #end_asyncio_work = time.time()

    #start_multi_requests = time.time()
    #asyncio.run(aiomultiprocess_test_just_requests())
    #end_multi_requests = time.time()

    #start_asyncio_requests = time.time()
    #asyncio.run(asyncio_test_just_requests())
    #end_asyncio_requests = time.time()

    start_multi_fibonacci = time.time()
    asyncio.run(aiomultiprocess_test_cpu_bound_work())
    end_multi_fibonacci = time.time()

    start_asyncio_fibonacci = time.time()
    asyncio.run(asyncio_test_cpu_bound_work())
    end_asyncio_fibonacci = time.time()

    #print(f'aiomultiprocess - doing work: {end_multi_work - start_multi_work}s')
    #print(f'asyncio - doing work: {end_asyncio_work - start_asyncio_work}s')
    #print(f'aiomultiprocess - just requests: {end_multi_requests - start_multi_requests}s')
    #print(f'asyncio - just requests: {end_asyncio_requests - start_asyncio_requests}s')
    print(f'aiomultiprocess - cpu-bound work: {end_multi_fibonacci - start_multi_fibonacci}s')
    print(f'asyncio - cpu-bound work: {end_asyncio_fibonacci - start_asyncio_fibonacci}s')

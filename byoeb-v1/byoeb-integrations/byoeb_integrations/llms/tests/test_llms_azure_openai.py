import os
import asyncio
import logging
import threading
import time
import pytest
from azure.identity import get_bearer_token_provider, AzureCliCredential
from byoeb_integrations.llms.azure_openai.async_azure_openai import AsyncAzureOpenAILLM
from byoeb_integrations import test_environment_path
from dotenv import load_dotenv

load_dotenv(test_environment_path)

AZURE_COGNITIVE_ENDPOINT = os.getenv('AZURE_COGNITIVE_ENDPOINT')
LLM_MODEL = os.getenv('LLM_MODEL')
LLM_ENDPOINT = os.getenv('LLM_ENDPOINT')
LLM_API_VERSION = os.getenv('LLM_API_VERSION')
token_provider = get_bearer_token_provider(
    AzureCliCredential(), AZURE_COGNITIVE_ENDPOINT
)

async_azure_openai_llm = AsyncAzureOpenAILLM(
        model=LLM_MODEL,
        azure_endpoint=LLM_ENDPOINT,
        token_provider=token_provider,
        api_version=LLM_API_VERSION
    )
async def atest_agenerate_response(msg):
    start = time.time()
    prompt = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt.append({"role": "user", "content": msg})
    response = await async_azure_openai_llm.agenerate_response(
        prompts=prompt,
        temperature=0.5
    )
    end = time.time()
    print(f"Thread ID: {threading.get_ident()} Response: {response.choices[0].message.content.strip()} Elapsed Time: {end-start}")

def test_agenerate_response():
    prompt1 = "Hello, how are you?"
    prompt2 = "What is your role?"

    start = time.time()
    thread1 = threading.Thread(target=lambda: asyncio.run(atest_agenerate_response(prompt1)))
    thread2 = threading.Thread(target=lambda: asyncio.run(atest_agenerate_response(prompt2)))
    thread3 = threading.Thread(target=lambda: asyncio.run(atest_agenerate_response(prompt1+prompt2)))

    barrier = threading.Barrier(3)
    # Start threads
    thread1.start()
    thread2.start()
    thread3.start()

    # Wait for both threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    end= time.time()

    print(f"Elapsed Time: {end-start}")
    # start = time.time()
    # atest_agenerate_response(prompt1)
    # atest_agenerate_response(prompt2)
    # atest_agenerate_response(prompt1+prompt2)
    # end = time.time()

if __name__ == "__main__":
    test_agenerate_response()
    test_agenerate_response()
    

# Guide: LLM Integration

> **Note**: This feature is currently under development and not yet available in the latest version of FastMango. The information on this page reflects the planned implementation.

FastMango is designed to be an AI-first framework, with built-in support for Large Language Models (LLMs). This guide will walk you through the planned features for integrating LLMs into your FastMango applications.

## The `LLMEngine`

The core of FastMango's LLM integration is the `LLMEngine` class. This class will provide a unified interface for interacting with various LLM providers, such as OpenAI, Anthropic, and Cohere.

You will be able to configure the `LLMEngine` in your `MangoApp` instance:

```python
from fastmango import MangoApp, LLMConfig

llm_config = LLMConfig(
    provider="openai",
    api_key="YOUR_API_KEY",
)

app = MangoApp(
    llm_config=llm_config,
)
```

## The `@app.llm_endpoint()` Decorator

FastMango will provide a special decorator, `@app.llm_endpoint()`, for creating API endpoints that are integrated with an LLM. This decorator will handle the details of prompting the LLM, parsing the response, and returning it to the user.

Here's an example of how you might use it:

```python
from pydantic import BaseModel

class StoryRequest(BaseModel):
    topic: str
    length: int

class StoryResponse(BaseModel):
    story: str

@app.llm_endpoint("/generate-story", response_model=StoryResponse)
def generate_story(request: StoryRequest):
    """
    Generates a story about the given topic with the specified length.
    """
    prompt = f"Write a {request.length}-word story about {request.topic}."
    return prompt
```

In this example:

1.  We define two Pydantic schemas: `StoryRequest` for the request body, and `StoryResponse` for the response.
2.  We create an endpoint at `/generate-story` using the `@app.llm_endpoint` decorator.
3.  The `generate_story` function takes a `StoryRequest` object as input and returns a prompt string.
4.  FastMango will automatically take the prompt, send it to the configured LLM, and parse the response into a `StoryResponse` object.

## Type-Safe LLM Integration with Pydantic AI

FastMango's LLM integration is built on top of [Pydantic AI](https://github.com/pydantic/pydantic-ai), which allows for type-safe interactions with LLMs. This means that you can use Pydantic models to define the structure of the data you expect to receive from the LLM, and Pydantic AI will automatically handle the parsing and validation.

This approach has several advantages:

-   **Reliability**: You can be confident that the data you receive from the LLM will be in the correct format.
-   **Developer Experience**: You can work with LLM responses as if they were regular Python objects, with all the benefits of type hinting and autocompletion.
-   **Reduced Boilerplate**: You don't have to write any code to parse the LLM's response.

## Next Steps

As the LLM integration features are developed, this guide will be updated with more detailed information and examples. In the meantime, you can learn more about the underlying technology by reading the [Pydantic AI documentation](https://github.com/pydantic/pydantic-ai).

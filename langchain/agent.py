"""LangChain agent — multi-step tool use, instrumented with Assay.

This agent answers a temperature conversion question using a tool.
It makes three LLM calls (plan → tool → synthesize), each producing
a signed receipt via AssayCallbackHandler.

Run:
    pip install -r requirements.txt
    export ANTHROPIC_API_KEY=sk-ant-...
    assay run -- python agent.py
    assay verify-pack proof_pack_*/
    assay explain proof_pack_*/
"""
from assay.integrations.langchain import AssayCallbackHandler

from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate


class _CompatHandler(AssayCallbackHandler):
    """Thin wrapper adding the ignore_* flags LangChain's dispatcher expects.

    AssayCallbackHandler is duck-typed. LangChain's callback manager checks for
    these boolean attributes before dispatching events; without them it raises
    AttributeError on every callback invocation (silently swallowed, but noisy).
    """
    ignore_llm = False
    ignore_chain = False
    ignore_agent = False
    ignore_retriever = False
    ignore_chat_model = False
    raise_error = False


@tool
def convert_celsius_to_fahrenheit(celsius: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


@tool
def convert_fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert a temperature from Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


def main():
    handler = _CompatHandler()

    llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        max_tokens=512,
    )

    tools = [convert_celsius_to_fahrenheit, convert_fahrenheit_to_celsius]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Use tools when you need to compute something."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # Pass handler via runtime config — AssayCallbackHandler is duck-typed and
    # does not subclass BaseCallbackHandler, so it cannot be passed to the
    # constructor directly (Pydantic validation rejects it).
    result = executor.invoke(
        {
            "input": (
                "Water boils at 100°C. What is that in Fahrenheit? "
                "Then: body temperature is 98.6°F — what is that in Celsius?"
            )
        },
        config={"callbacks": [handler]},
    )

    print("\n--- Agent answer ---")
    print(result["output"])


if __name__ == "__main__":
    main()

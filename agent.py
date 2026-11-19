
import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from tools import search_web, check_source, is_trusted_source


# =================================
# 1. LOAD ENVIRONMENT VARIABLES
# =================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "Groq API key not found. Check your .env file."
    )


# =================================
# 2. INITIALIZE GROQ MODEL
# =================================

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
    max_tokens=4096,
    api_key=api_key
)


# =================================
# 3. CONNECT AI TOOLS
# =================================

tools = [search_web, check_source]

llm_with_tools = llm.bind_tools(tools)


# =================================
# 4. EXTRACT SOURCES FROM SEARCH
# =================================

def extract_sources(search_results):

    sources = []
    seen_urls = set()

    for line in search_results.splitlines():

        if line.startswith("Title: "):
            title = line.replace("Title: ", "").strip()

        elif line.startswith("Link: "):

            url = line.replace("Link: ", "").strip()

            if (
                url.startswith(("http://", "https://"))
                and url not in seen_urls
            ):

                seen_urls.add(url)

                sources.append({
                    "title": title if "title" in locals() else "Web source",
                    "url": url
                })

    return sources


# =================================
# 5. VERIFY SOURCES
# =================================

def verify_sources(sources):

    verified_sources = []

    for source in sources:

        url = source["url"]

        try:

            result = check_source.invoke({
                "url": url
            })

            if "URL reachable" in result:
                status = "Reachable"

            elif "HTTP Status" in result:
                status = "HTTP error"

            else:
                status = "Check failed"

            category = (
                "Prioritized domain"
                if is_trusted_source(url)
                else "Other domain"
            )

            verified_sources.append({
                "title": source["title"],
                "url": url,
                "status": status,
                "category": category
            })

            print("SOURCE VERIFICATION:", result)

        except Exception as e:

            verified_sources.append({
                "title": source["title"],
                "url": url,
                "status": f"Check failed: {str(e)}",
                "category": (
                    "Prioritized domain"
                    if is_trusted_source(url)
                    else "Other domain"
                )
            })

    return verified_sources


# =================================
# 6. AI AGENT WITH MEMORY
# =================================

def get_ai_response(
    question,
    research_mode="Quick Research",
    chat_history=None
):

    try:

        if chat_history is None:
            chat_history = []

        # PREPARE CONVERSATION MEMORY

        conversation_history = ""

        for chat in chat_history[-10:]:

            conversation_history += f"""
User: {chat['question']}

Assistant: {chat['answer']}
"""

        # CREATE PROMPT

        prompt = f"""
You are NEXUS AI, an intelligent research assistant.

PREVIOUS CONVERSATION:
{conversation_history}

CURRENT RESEARCH MODE:
{research_mode}

CURRENT USER QUESTION:
{question}


INSTRUCTIONS:

1. Understand the user's question.
2. Always read the previous conversation before answering.
3. Resolve words like "it", "its", "they", "them",
   and "that" using the previous conversation.
4. If the user asks a follow-up question, continue
   discussing the previous topic.
5. Do not ask for clarification when the previous
   conversation clearly identifies the topic.
6. Use web search when online information is needed.
7. Use simple English.
8. Include useful source links when available.
9. Do not invent information.

"""

        # CALL AI MODEL

        response = llm_with_tools.invoke([
            HumanMessage(content=prompt)
        ])

        print("AI TOOL CALLS:", response.tool_calls)

        tool_results = []
        all_sources = []

        # EXECUTE TOOL CALLS

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            arguments = tool_call.get("args", {})

            # WEB SEARCH

            if tool_name == "search_web":

                query = arguments.get("query")

                if not query:
                    continue

                result = search_web.invoke({
                    "query": query
                })

                print("SEARCH RESULTS:", result)

                tool_results.append(str(result))

                if not str(result).startswith("Search error"):

                    found_sources = extract_sources(str(result))

                    all_sources.extend(found_sources)

            # DIRECT SOURCE CHECK

            elif tool_name == "check_source":

                url = arguments.get("url")

                if url and url.startswith(("http://", "https://")):

                    all_sources.append({
                        "title": "User-requested source",
                        "url": url
                    })

        # REMOVE DUPLICATE SOURCES

        unique_sources = []
        seen_urls = set()

        for source in all_sources:

            if source["url"] not in seen_urls:

                seen_urls.add(source["url"])
                unique_sources.append(source)

        # VERIFY SOURCES

        verified_sources = verify_sources(unique_sources)

        # GENERATE FINAL ANSWER

        if tool_results:

            final_prompt = f"""
You are NEXUS AI, an intelligent research assistant.

USER QUESTION:
{question}

RESEARCH MODE:
{research_mode}

PREVIOUS CONVERSATION:
{conversation_history}

SEARCH RESULTS:
{" ".join(tool_results)}

SOURCE VERIFICATION DETAILS:
{verified_sources}

Write a clear research answer in simple English.

Instructions:

1. Explain the topic clearly.
2. Use the available search results.
3. Include useful source links.
4. Do not invent facts.
5. Do not say a source is factually verified only because its URL is reachable.
6. Do not perform another search.
"""

            final_response = llm.invoke([
                HumanMessage(content=final_prompt)
            ])

            answer = final_response.content
            print("FINAL ANSWER:", answer)

        else:

            answer = response.content

        # RETURN ANSWER AND SOURCES SEPARATELY

        return {
            "answer": answer,
            "sources": verified_sources
        }

    except Exception as e:

        print("AGENT ERROR:", str(e))

        return {
            "answer": (
                "Error generating research answer: "
                f"{str(e)}"
            ),
            "sources": []
        }

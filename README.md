# GenAI & Agentic AI Hands-on

Runnable notebooks and projects from my LinkedIn series on Generative AI and Agentic AI.
The series runs in order, from LLM foundations to production multi-agent systems. Every project is self-contained: clone the repo, install `requirements.txt`, set your API key and run.

| # | Track | Projects |
|---|---|---|
| 01 | [GenAI & LLM Foundations](01-genai-llm-foundations/) | 8 projects |
| 02 | [Prompt Engineering](02-prompt-engineering/) | 8 projects |
| 03 | [RAG System](03-rag-systems/) | 8 projects |
| 04 | [AI Agents Foundations & First ReAct Agent](04-agent-foundations-react/) | 8 projects |
| 05 | [LangGraph Core Workflow Patterns](05-langgraph-workflow-patterns/) | 8 projects |
| 06 | [MultiAgent Architectures](06-multi-agent-architectures/) | 8 projects |
| 07 | [Multi-Framework Agent Development](07-multi-framework-agents/) | 8 projects |
| 08 | [Context Engineering & Agent Evaluations](08-context-engineering-evals/) | 8 projects |
| 09 | [Guardrails, Observability and MCP-A2A](09-guardrails-observability-mcp-a2a/) | 8 projects |

## Running a project
```sh
git clone https://github.com/<your-github-username>/genai-handson.git
cd genai-handson/<track>/<project>
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your ANTHROPIC_API_KEY
```

Follow along on LinkedIn for a new project four times a week.

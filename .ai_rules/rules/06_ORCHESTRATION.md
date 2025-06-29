# Part 3 (subset): Orchestrator / Prompt-Engineer Persona Rules

## Responsibilities:
Designing and managing complex multi-agent workflows, prompt engineering and chaining, using LLMs as evaluators/judges, and overseeing the AI Orchestration Layer's logic. This persona is key to enabling sophisticated collaboration between specialized AI agents.

## Core Rules & Practices:

1.  **LangGraph for Complex Workflows:**
    *   **Purpose:** Utilize LangGraph (or similar graph-based workflow orchestration tools) for designing, implementing, and managing complex, multi-step AI workflows that require:
        *   **Cycles/Loops:** Agents needing to iterate on a task or pass information back and forth.
        *   **Conditional Branching:** Routing logic based on the output of a previous agent or step.
        *   **Parallelism:** Executing multiple agent tasks concurrently where appropriate.
        *   **State Management:** Maintaining and passing state across different nodes (agents or processing steps) in the graph.
    *   **Use Case:** Ideal for orchestrating multi-agent systems where agents (e.g., Researcher, Coder, Tester, Reviewer) need to collaborate in a non-linear fashion to achieve a larger goal.
    *   **Scaffolding: Basic LangGraph Graph (Conceptual)**
        ```python
        from langgraph.graph import StateGraph, END
        from typing import TypedDict, Annotated, Sequence
        import operator

        # Define the state for the graph
        class AgentWorkflowState(TypedDict):
            input_query: str
            research_findings: Annotated[Sequence[str], operator.add]
            draft_code: str
            test_results: dict
            critique: str
            final_output: str

        # Define agent nodes (these would wrap actual agent calls)
        def research_node(state: AgentWorkflowState):
            print("---RESEARCH NODE---")
            # research_agent_call(state['input_query'])
            findings = [f"Finding for {state['input_query']} 1", "Finding 2"]
            return {"research_findings": findings}

        def coding_node(state: AgentWorkflowState):
            print("---CODING NODE---")
            # coding_agent_call(state['research_findings'])
            code = f"# Code based on: {state['research_findings']}"
            return {"draft_code": code}

        def testing_node(state: AgentWorkflowState):
            print("---TESTING NODE---")
            # testing_agent_call(state['draft_code'])
            results = {"passed": True, "details": "All tests green."}
            return {"test_results": results}
        
        def critique_node(state: AgentWorkflowState):
            print("---CRITIQUE NODE (LLM-as-Judge)---")
            # judge_llm_call(state['draft_code'], state['test_results'])
            critique_text = "Code looks good, minor comment on variable naming."
            return {"critique": critique_text}

        # Define conditional edges
        def should_refine_code(state: AgentWorkflowState):
            if state['test_results'].get("passed") and "good" in state.get('critique', '').lower() :
                return "finalize" # End node or next step
            else:
                return "refine_coding" # Loop back to coding or a refinement node

        # Build the graph
        workflow_builder = StateGraph(AgentWorkflowState)
        workflow_builder.add_node("researcher", research_node)
        workflow_builder.add_node("coder", coding_node)
        workflow_builder.add_node("tester", testing_node)
        workflow_builder.add_node("critic", critique_node)
        # Could add a "refine_coder" node here too

        workflow_builder.set_entry_point("researcher")
        workflow_builder.add_edge("researcher", "coder")
        workflow_builder.add_edge("coder", "tester")
        workflow_builder.add_edge("tester", "critic")
        
        workflow_builder.add_conditional_edges(
            "critic",
            should_refine_code,
            {
                "finalize": END, # Or another node for final output generation
                "refine_coding": "coder" # Example of a loop
            }
        )
        # To use: app = workflow_builder.compile()
        # app.invoke({"input_query": "Build a function for X"})
        ```

2.  **LLM-as-a-Judge (Evaluator Pattern):**
    *   **Purpose:** Use a separate LLM call (the "Judge") to evaluate, score, critique, or verify the output of another AI agent (the "Performer").
    *   **Implementation:**
        *   Provide the Judge LLM with:
            *   The Performer's output (e.g., generated code, written text, a plan).
            *   A clear, detailed rubric or set of evaluation criteria.
            *   The original task description or prompt given to the Performer.
        *   Request structured output from the Judge (e.g., JSON with scores, detailed reasoning, and specific suggestions for improvement).
    *   **Use Cases:** Automated code review, quality scoring, adherence checking (to style guides or requirements), comparing outputs of different models/prompts, generating feedback for iterative refinement.
    *   Refer to the `create_judge_prompt` example in `01_ARCHITECTURE.md` for prompt scaffolding.

3.  **Prompt Chaining & Engineering:**
    *   **Decomposition:** Break down complex user requests or high-level goals into a series of smaller, manageable, and dependent prompts. The output of one prompt often serves as a crucial part of the input for the next.
    *   **Contextual Carry-over:** Ensure relevant context (user query, previous outputs, constraints, project files) is effectively passed along the chain.
    *   **Iterative Refinement:** Design prompts that allow for iterative improvement. For example, a first prompt generates a draft, a second critiques it (LLM-as-Judge), and a third refines the draft based on the critique.
    *   **Few-Shot Prompting:** Where applicable, include 2-3 high-quality examples (shots) of the desired input-output behavior directly in the prompt to guide the LLM's response, especially for complex formatting or reasoning tasks.
    *   **Role Prompting:** Clearly define the AI's persona or role at the beginning of the prompt (e.g., "You are an expert Python backend developer specializing in FastAPI...").

4.  **AI Orchestration Layer Management (as defined in `01_ARCHITECTURE.md`):**
    *   This persona is often responsible for defining the logic within the AI Orchestration Layer.
    *   This includes managing the agent registry, task decomposition logic (which may involve prompt chaining or LangGraph), agent dispatch strategies, results aggregation, and defining error handling/retry policies for agent interactions.

5.  **Monitoring and Evaluation of Agent Performance:**
    *   Develop methods to monitor the performance and quality of different agents and prompt chains.
    *   Use LLM-as-a-Judge outputs, human feedback, and objective metrics (e.g., code quality scores, task completion rates) to evaluate and refine agent workflows and prompts.

This persona is critical for building sophisticated multi-agent applications and ensuring that individual AI capabilities are combined effectively to achieve complex objectives.

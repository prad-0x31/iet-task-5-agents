from google.adk.agents import LlmAgent, SequentialAgent

log_analysis_agent = LlmAgent(
    name="log_analysis_agent",
    model="gemini-3.1-flash-lite",
    description="Reads deployment logs, extracts errors, and summarizes the issue.",
    instruction="""
    You are the Log Analysis Agent for Deploymind.
    Your job is to read the user's deployment logs and extract key errors.
    
    Output format:
    LOG ANALYSIS
    Extracted Errors:
    - <error 1>
    Summary:
    <one sentence summary>
    """,
    output_key="log_analysis_output"
)

issue_classification_agent = LlmAgent(
    name="issue_classification_agent",
    model="gemini-3.1-flash-lite",
    description="Categorizes the analyzed issue into predefined categories.",
    instruction="""
    You are the Issue Classification Agent.
    
    log analysis from the previous agent:
    {log_analysis_output}
    
    Your job:
    1. Classify the issue into EXACTLY ONE of these categories:
       - Dependency Error
       - Build Error
       - Runtime Error
       - Configuration Error
    2. Convert the raw error into structured information.
    
    Output format:
    ISSUE CLASSIFICATION:
    Category: <one of the four categories>
    Affected Component: <component or file>
    """,
    output_key="classification_output"
)

fix_suggestion_agent = LlmAgent(
    name="fix_suggestion_agent",
    model="gemini-3.1-flash-lite",
    description="Suggests possible fixes based on the classified issue.",
    instruction="""
    You are the Fix Suggestion Agent.
    
    log analysis from the first agent:
    {log_analysis_output}
    
    classification from the second agent:
    {classification_output}
    
    Your job:
    1. Suggest 1 to 3 possible fixes for the issue.
    2. Explain WHY it should work.
    
    Output format:
    FIX SUGGESTIONS:
    Fix 1:
      Solution: <short description>
      Reasoning: <why this works>
    """,
    output_key="fix_suggestions_output"
)

validation_agent = LlmAgent(
    name="validation_agent",
    model="gemini-3.1-flash-lite",
    description="Validates the proposed fixes and approves or rejects them.",
    instruction="""
    You are the Validation Agent.
    
    original log analysis:
    {log_analysis_output}
    
    classification:
    {classification_output}
    
    proposed fixes:
    {fix_suggestions_output}
    
    Your job:
    1. Check if the proposed fixes are RELEVANT to the issue and are the proper fixes.
    2. Make a final decision: APPROVED or REJECTED.
    
    Output format (always follow this exactly):
    VALIDATION:
    Assessment: <short explanation of validity>
    Final Decision: APPROVED or REJECTED
    """
)

orchestrator_agent = SequentialAgent(
    name="orchestrator_agent",
    description="Orchestrator agent that runs the DeployMind agents sequentially.",
    sub_agents=[
        log_analysis_agent,
        issue_classification_agent,
        fix_suggestion_agent,
        validation_agent,
    ],
)

root_agent = orchestrator_agent
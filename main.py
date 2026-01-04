import os
import yaml
import subprocess
import readline  # noqa: F401
from dotenv import load_dotenv
from typing import List, Dict
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage

global_base_dir = os.path.dirname(os.path.abspath(__file__))


# 1. Define tools that allow the agent to "use" skills by exploring the filesystem
@tool
def run_shell_command(command: str) -> str:
    """Executes a shell command and returns the output.
    Use this to run python scripts or other system commands.
    Make sure to use paths relative to the current directory."""
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, cwd=global_base_dir
        )
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"


@tool
def read_skill_file(file_path: str) -> str:
    """Reads a file from a skill directory.
    The file_path should be in the format 'skill-name/filename.md' (e.g., 'text-processor/instructions.md').
    Use this to get detailed instructions or data for a skill."""
    # Ensure we only read from the skills directory for safety in this example
    base_dir = os.path.abspath(global_base_dir)
    target_path = os.path.abspath(os.path.join(base_dir, file_path))

    if not target_path.startswith(base_dir):
        return (
            "Error: Access denied. You can only read files within the skills directory."
        )

    try:
        with open(target_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def list_skill_contents(skill_name: str) -> List[str]:
    """Lists the files available in a specific skill directory."""
    skill_dir = os.path.join(global_base_dir, skill_name)
    try:
        return os.listdir(skill_dir)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]


# 2. Skill Loader: Discover skills and extract metadata from SKILL.md
def load_agent_skills(skills_root: str) -> List[Dict]:
    skills = []
    if not os.path.exists(skills_root):
        return skills

    for item in os.listdir(skills_root):
        skill_path = os.path.join(skills_root, item)
        if os.path.isdir(skill_path):
            skill_md_path = os.path.join(skill_path, "SKILL.md")
            if os.path.exists(skill_md_path):
                with open(skill_md_path, "r") as f:
                    content = f.read()
                    # Simple YAML frontmatter extraction
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            metadata = yaml.safe_load(parts[1])
                            metadata["path"] = item
                            skills.append(metadata)
    return skills


# 3. Construct the System Prompt with Skills
def create_skill_system_prompt(skills: List[Dict]) -> str:
    prompt = "You are a helpful assistant with access to 'Agent Skills'.\n"
    prompt += "At startup, you have been equipped with the following skills:\n\n"

    for skill in skills:
        prompt += f"- {skill['name']}: {skill['description']}\n"

    prompt += "\nTo use a skill, use the `list_skill_contents` tool to see what's inside its directory, "
    prompt += "and `read_skill_file` to read specific instructions or data files within that skill.\n"
    prompt += "Always follow the instructions found within a skill's directory when a task matches that skill."
    return prompt


def main():
    # Load skills
    skills_root = global_base_dir
    available_skills = load_agent_skills(skills_root)

    # Initialize LLM (ChatOpenAI)
    # Note: Ensure OPENAI_API_KEY is set in your environment variables
    load_dotenv()

    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model_name=os.getenv("OPENAI_MODEL_NAME"),
        temperature=0,
    )

    # Define Tools
    tools = [read_skill_file, list_skill_contents, run_shell_command]

    # Create Prompt
    system_message = create_skill_system_prompt(available_skills)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    print("\n--- Example Setup Complete ---")
    print(f"System Prompt Snippet:\n{system_message}")

    # Create Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    chat_history = []

    print("\n--- Interactive Chat Started (Press Ctrl+C to exit) ---")

    try:
        while True:
            user_input = input("\nUser: ")
            if not user_input.strip():
                continue

            if user_input.lower() in ["exit", "quit"]:
                break

            # Run Agent
            response = agent_executor.invoke(
                {"input": user_input, "chat_history": chat_history}
            )

            output = response["output"]
            print(f"Assistant: {output}")

            # Update history
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=output))

    except KeyboardInterrupt:
        print("\n\nExiting chat... Goodbye!")


if __name__ == "__main__":
    main()

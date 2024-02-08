import os

import autogen
from autogen import AssistantAgent, UserProxyAgent
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
from autogen.code_utils import extract_code

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location=".",
)
if not config_list:
    os.environ["MODEL"] = "gpt-4"
    os.environ["OPENAI_API_KEY"] = "API_KEY"
    os.environ["OPENAI_BASE_URL"] = "https://api.openai.com/v1" # optional

    config_list = autogen.config_list_from_models(
        model_list=[os.environ.get("MODEL", "gpt-4")],
    )

llm_config = {
    "timeout": 60,
    "cache_seed": 42,
    "config_list": config_list,
    "temperature": 0,
}

def termination_msg(x):
    _msg = str(x.get("content", "")).upper().strip().strip("\n").strip(".")
    return isinstance(x, dict) and (_msg.endswith("TERMINATE") or _msg.startswith("TERMINATE"))

def _is_termination_msg(message):
    if isinstance(message, dict):
        message = message.get("content")
        if message is None:
            return False
    cb = extract_code(message)
    contain_code = False
    for c in cb:
        # todo: support more languages
        if c[0] == "python":
            contain_code = True
            break
    return not contain_code

agents = []


agent = UserProxyAgent(
    name="Admin",
    is_termination_msg=termination_msg,
    human_input_mode="TERMINATE",
    system_message="""A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.""",
    default_auto_reply="Good, thank you. Reply `TERMINATE` to finish.",
    max_consecutive_auto_reply=5,
    code_execution_config={'work_dir': 'coding', 'use_docker': False},
)


agents.append(agent)


agent = AssistantAgent(
    name="Engineer",
    system_message="""Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.""",
    llm_config=llm_config,
    is_termination_msg=termination_msg,
)


agents.append(agent)


agent = AssistantAgent(
    name="Scientist",
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""",
    llm_config=llm_config,
    is_termination_msg=termination_msg,
)


agents.append(agent)


agent = AssistantAgent(
    name="Planner",
    system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.""",
    llm_config=llm_config,
    is_termination_msg=termination_msg,
)


agents.append(agent)


agent = AssistantAgent(
    name="Critic",
    system_message="""Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.""",
    llm_config=llm_config,
    is_termination_msg=termination_msg,
)


agents.append(agent)


agent = UserProxyAgent(
    name="Executor",
    is_termination_msg=termination_msg,
    human_input_mode="TERMINATE",
    system_message="""Executor. Execute the code written by the engineer and report the result.""",
    default_auto_reply="Good, thank you. Reply `TERMINATE` to finish.",
    max_consecutive_auto_reply=5,
    code_execution_config={'work_dir': 'coding', 'use_docker': False},
)


agents.append(agent)


init_sender = None
for agent in agents:
    if "UserProxy" in str(type(agent)):
        init_sender = agent
        break

if not init_sender:
    init_sender = agents[0]


groupchat = autogen.GroupChat(
    agents=agents, messages=[], max_round=12, speaker_selection_method="round_robin", allow_repeat_speaker=False
)  # todo: auto, sometimes message has no name
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

recipient = manager

if isinstance(init_sender, (RetrieveUserProxyAgent, MathUserProxyAgent)):
    init_sender.initiate_chat(recipient, problem="hello")
else:
    init_sender.initiate_chat(recipient, message="hello")

import sys

from langchain_google_genai import ChatGoogleGenerativeAI
from Functions.code_gen_execution.arbitrary_code import arbitrary_code
from Functions.web_interface.search import custom_search_tool
from Functions.discord_module.discord_message import discord_messaging
from dependencies import *
from models.llm import gemini_pro
import builtins

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
from PySide6.QtGui import QIcon 
from PySide6.QtCore import QSize

llm = gemini_pro

llm.temperature = 0.3


# Define the tools to be used by the agent
tools = [custom_search_tool, discord_messaging, arbitrary_code]


# Pull the prompt from the hub
prompt = hub.pull("hwchase17/react-chat")

# Partially apply the prompt with the tools description and tool names
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)

# Bind the LLM with a stop condition
llm_with_stop = llm.bind(stop=["\nObservation"])

# Define the template for tool response
# Define the agent
agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_log_to_messages(x["intermediate_steps"]),
        "chat_history": lambda x: x["chat_history"],
    }
    | prompt
    | llm_with_stop
    | ReActSingleInputOutputParser()
)

# Initialize the conversation memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, output_key='output')

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory, return_intermediate_steps=True)

class LLMApp(QWidget):
    def __init__(self):
        super(LLMApp,self).__init__()
        
        self.init_llm()
        self.init_ui()
        
    def init_llm(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro")
        self.llm.temperature = 0.3
        self.tools = [custom_search_tool, discord_messaging, arbitrary_code]
        self.prompt = hub.pull("hwchase17/react-chat")
        self.prompt = self.prompt.partial(
            tools=render_text_description(self.tools),
            tool_names=", ".join([t.name for t in self.tools]),
        )
        self.llm_with_stop = self.llm.bind(stop=["\nObservation"])        
        
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20,20,20,20)

        self.setWindowTitle('LLM Agent')
        self.setGeometry(100, 100, 400, 900)

        bottom_layout = QHBoxLayout()

        self.query_input = QLineEdit()
        self.query_input.setStyleSheet("border:2px solid green; color: white; border-radius:20px; padding: 10px; font-size:18px")

        self.execute_button = QPushButton()
        self.execute_button.setStyleSheet("border:2px solid green; border-radius:40px; padding: 10px;")
        button_icon = QIcon("./paper-plane-solid.svg")
        self.execute_button.setIcon(button_icon)
        self.execute_button.setIconSize(QSize(25, 25))

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("color:white; font-size: 18px;")

        self.execute_button.clicked.connect(self.handle_query)
        self.query_input.returnPressed.connect(self.handle_query)

        bottom_layout.addWidget(self.query_input)
        bottom_layout.addWidget(self.execute_button)


        main_layout.addWidget(self.output_text)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)
    def handle_query(self):
        query = self.query_input.text()
        builtins.global_prompt = query
        try:
            output = agent_executor.invoke({f"input": {query}})["output"]
            self.output_text.setPlainText(f"{output}")
        except ValueError as e:
            self.output_text.setPlainText(f"**output:**\n\n```An error occurred while parsing the LLM output: {e}```")
        except KeyboardInterrupt:
            print("exiting")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    llm_app = LLMApp()
    llm_app.show()
    sys.exit(app.exec_())
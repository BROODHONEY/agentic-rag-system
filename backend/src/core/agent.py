"""Main agent orchestrator for Agentic RAG system."""
from typing import List, Dict, Any, Optional
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import Tool
import yaml
from pathlib import Path

from src.core.llm import get_llm
from src.tools.semantic_search import create_semantic_search_tool
from src.memory.conversation import ConversationMemory
from src.utils.logger import logger
from src.utils.exceptions import AgenticRAGException


class AgenticRAG:
    """Main Agentic RAG orchestrator."""
    
    def __init__(
        self,
        tools: Optional[List[Tool]] = None,
        use_memory: bool = True,
    ):
        """Initialize Agentic RAG system."""
        self.llm = get_llm()
        self.use_memory = use_memory
        
        # Initialize memory
        if use_memory:
            self.memory = ConversationMemory()
        else:
            self.memory = None
        
        # Load prompts
        self.prompts = self._load_prompts()
        
        # Initialize tools
        if tools is None:
            tools = self._get_default_tools()
        self.tools = tools
        
        # Create agent
        self.agent_executor = self._create_agent()
        
        logger.info("Initialized Agentic RAG system")
    
    def _load_prompts(self) -> Dict[str, Any]:
        """Load prompt templates from YAML file."""
        try:
            prompts_file = Path("config/prompts.yaml")
            with open(prompts_file, 'r') as f:
                prompts = yaml.safe_load(f)
            return prompts
        except Exception as e:
            logger.warning(f"Could not load prompts.yaml: {e}, using defaults")
            return {
                "system_prompts": {
                    "agent": "You are a helpful AI assistant with access to a knowledge base."
                }
            }
    
    def _get_default_tools(self) -> List[Tool]:
        """Get default tools for the agent."""
        semantic_tool = create_semantic_search_tool()
        return [semantic_tool.as_langchain_tool()]
    
    def _create_agent(self) -> AgentExecutor:
        """Create the LangChain agent executor."""
        try:
            system_prompt = self.prompts.get("system_prompts", {}).get(
                "agent",
                "You are a helpful AI assistant."
            )
            
            # Create prompt template for ReAct agent
            template = f"""{system_prompt}

You have access to the following tools:

{{tools}}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {{input}}
Thought:{{agent_scratchpad}}"""
            
            prompt = PromptTemplate.from_template(template)
            
            # Create ReAct agent
            agent = create_react_agent(
                llm=self.llm.llm,
                tools=self.tools,
                prompt=prompt,
            )
            
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=5,
            )
            
            logger.info("Created agent executor")
            return agent_executor
            
        except Exception as e:
            logger.error(f"Error creating agent: {e}")
            raise AgenticRAGException(f"Failed to create agent: {e}")
    
    def query(
        self,
        question: str,
        conversation_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Query the Agentic RAG system.
        
        Flow with embeddings:
        1. User question is received
        2. Agent decides to use semantic_search tool
        3. semantic_search converts query to embeddings using HuggingFace model
        4. ChromaDB performs vector similarity search using embeddings
        5. Most relevant document chunks are retrieved
        6. Retrieved chunks are passed to LLM as context
        7. LLM generates answer based on retrieved context
        """
        try:
            logger.info(f"Processing query: {question}")
            
            # Execute query
            response = self.agent_executor.invoke({"input": question})
            
            # Extract answer
            answer = response.get("output", "I couldn't generate an answer.")
            
            # Save to memory if enabled
            if self.use_memory and conversation_id:
                self.memory.add_message(conversation_id, "user", question)
                self.memory.add_message(conversation_id, "assistant", answer)
            
            result = {
                "answer": answer,
                "question": question,
                "metadata": {
                    "model": self.llm.model,
                    "tools_used": len(self.tools),
                }
            }
            
            logger.info("Successfully processed query")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            raise AgenticRAGException(f"Query processing failed: {e}")
    
    def clear_memory(self, conversation_id: str) -> None:
        """Clear conversation memory."""
        if self.use_memory:
            self.memory.clear_history(conversation_id)
            logger.info(f"Cleared memory for conversation: {conversation_id}")
    
    def get_tool_names(self) -> List[str]:
        """Get list of tool names."""
        return [tool.name for tool in self.tools]


def create_agentic_rag(
    tools: Optional[List[Tool]] = None,
    use_memory: bool = True,
) -> AgenticRAG:
    """Factory function to create Agentic RAG system."""
    return AgenticRAG(tools=tools, use_memory=use_memory)
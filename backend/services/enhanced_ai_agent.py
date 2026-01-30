from typing import Dict, Any, List
import sys
import os
from pathlib import Path
import re

# Add backend directory to path to resolve relative imports
backend_dir = Path(__file__).parent.parent
backend_path = str(backend_dir.resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from mcp.tools import add_task_tool, list_tasks_tool, update_task_tool, delete_task_tool, complete_task_tool


class AIAgent:
    """
    AI Agent that processes natural language and maps to appropriate MCP tools
    """

    def __init__(self):
        self.tools = {
            "add_task": add_task_tool,
            "list_tasks": list_tasks_tool,
            "update_task": update_task_tool,
            "delete_task": delete_task_tool,
            "complete_task": complete_task_tool
        }
        # System prompt
        self.system_prompt = """You are an AI Todo Assistant.

Your job is to help users manage their tasks using natural language.
You support ONLY these actions:
- Add a task
- Show all tasks
- Complete a task
- Delete a task

Behavior rules:
1. If the user greets you (hi, hello, hey, good morning, etc), reply politely and explain what you can do.
2. If the user input matches a task action, respond with a clear and structured response.
3. If the user input does NOT match any supported action, DO NOT throw an error.
   Instead, politely guide the user with examples.
4. Never respond with technical errors or backend messages.
5. Always be friendly, helpful, and concise.

Examples:

User: hi
Assistant: Hello! 👋 I'm your AI Todo assistant.
You can try:
- Add a task to buy groceries
- Show me my tasks
- Complete task 1
- Delete task 2

User: add a task to buy groceries
Assistant: ✅ Task added: "buy groceries"

User: show my tasks
Assistant: 📋 Here are your tasks:
1. buy groceries

User: xyz123
Assistant: Sorry 😅 """

    def detect_intent(self, message: str) -> Dict[str, Any]:
        """
        Detect user intent from natural language message following the specified intents
        """
        message_lower = message.lower().strip()

        # GREETING intent - Check for greetings first, but only if it's a greeting-focused message
        greeting_patterns = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings', 'morning', 'afternoon', 'evening']

        # Check if message is primarily a greeting (starts with greeting or is mostly greeting)
        message_words = message_lower.split()
        greeting_matches = [word for word in message_words if word in greeting_patterns]

        # If the message is mostly greetings or starts with a greeting and is short
        if greeting_matches and (len(message_words) <= 3 or message_lower.startswith(tuple(greeting_patterns))):
            return {
                "intent": "GREETING",
                "params": {}
            }

        # ADD_TASK intent - More comprehensive patterns
        add_patterns = [
            r'(?:add|create|make|new)\s+(?:a\s+|the\s+|an\s+)?(?:task|todo|to-do|item)\s+(?:to\s+|for\s+|about\s+|that\s+|which\s+)?(.+?)(?:\s+to\s+my\s+list|$)',
            r'(?:add|create|make|new)\s+(.+?)(?:\s+to\s+my\s+list|$)',
            r'(?:i\s+need\s+to|i\s+want\s+to|please\s+|can\s+i|could\s+i)\s*(?:add|create|make)\s+(?:a\s+|the\s+|an\s+)?(?:task|todo|to-do|item)\s+(?:to\s+|for\s+)?(.+)',
            r'add\s+(.+)',
        ]

        for pattern in add_patterns:
            match = re.search(pattern, message_lower)
            if match:
                title = match.group(1).strip() if match.lastindex else match.group(0)[match.end(0)-len(match.group(0)):].strip()

                # If there are multiple groups, use the first captured group
                if match.groups():
                    title = match.group(1).strip()

                # Clean up the title
                if title:
                    title = re.sub(r'(to\s+my\s+list|please|thanks|now|for\s+me)', '', title).strip()
                    if len(title) > 0:  # Only return if we have a meaningful title
                        return {
                            "intent": "ADD_TASK",
                            "params": {"title": title}
                        }

        # LIST_TASKS intent - More comprehensive patterns
        list_keywords = ['list', 'show', 'display', 'view', 'see', 'my', 'tasks', 'todos', 'to-dos']
        list_phrases = ['show me', 'show my', 'list my', 'display my', 'view my', 'see my', 'what are', 'what\'re', 'tell me']

        # Check for list-related phrases
        if any(phrase in message_lower for phrase in list_phrases) or \
           ('list' in message_lower and any(keyword in message_lower for keyword in ['my', 'tasks', 'todos'])) or \
           ('show' in message_lower and 'task' in message_lower) or \
           (message_lower.startswith(('list ', 'show ', 'display ', 'view ')) and any(keyword in message_lower for keyword in ['task', 'my'])):
            return {
                "intent": "LIST_TASKS",
                "params": {}
            }

        # DELETE_TASK intent - More comprehensive patterns
        delete_patterns = [
            r'(?:delete|remove|cancel|eliminate|get rid of)\s+(?:task|the\s+task|#)?\s*(\d+)',
            r'(?:delete|remove|cancel|eliminate|get rid of)\s+(?:task\s+|#)?(\d+)',
            r'delete\s+(?:task\s+)?"?([^"]+?)"?',
        ]

        delete_keywords = ['delete', 'remove', 'cancel']
        if any(keyword in message_lower for keyword in delete_keywords):
            task_id = self._extract_task_id(message_lower)
            if task_id:
                return {
                    "intent": "DELETE_TASK",
                    "params": {"task_id": task_id}
                }
            else:
                # If delete keyword is used but no ID found, return incomplete
                return {
                    "intent": "DELETE_TASK",
                    "params": {"task_id": ""}
                }

        # UPDATE_TASK intent - More comprehensive patterns
        update_keywords = ['update', 'change', 'modify', 'edit', 'alter', 'adjust']
        if any(keyword in message_lower for keyword in update_keywords):
            task_id = self._extract_task_id(message_lower)
            # Try to extract new content
            content_match = re.search(r'(?:update|change|edit)\s+(?:task\s+)?\d+\s+(?:to|with|as|into)?\s*(.+)', message_lower)
            new_content = content_match.group(1).strip() if content_match else ""

            return {
                "intent": "UPDATE_TASK",
                "params": {"task_id": task_id, "new_content": new_content}
            }

        # COMPLETE_TASK intent - More comprehensive patterns
        complete_patterns = [
            r'(?:complete|finish|done|accomplish|mark.*done|check.*off)\s+(?:task|the\s+task|#)?\s*(\d+)',
            r'(?:complete|finish|done|accomplish|mark.*done|check.*off)\s+(?:task\s+|#)?(\d+)',
        ]

        for pattern in complete_patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_id = match.group(1).strip()
                return {
                    "intent": "COMPLETE_TASK",
                    "params": {"task_id": task_id}
                }

        complete_keywords = ['complete', 'finish', 'done', 'accomplish', 'marked.*done', 'check.*off']
        if any(re.search(keyword, message_lower) for keyword in complete_keywords if '*' in keyword) or \
           any(keyword in message_lower for keyword in complete_keywords if '*' not in keyword):
            task_id = self._extract_task_id(message_lower)
            if task_id:
                return {
                    "intent": "COMPLETE_TASK",
                    "params": {"task_id": task_id}
                }
            else:
                # If complete keyword is used but no ID found, return incomplete
                return {
                    "intent": "COMPLETE_TASK",
                    "params": {"task_id": ""}
                }

        # FINAL FALLBACK: Check if any task-related keywords exist but no specific action was clear
        task_related_keywords = ['task', 'todo', 'to-do', 'item', 'list', 'add', 'create', 'delete', 'remove', 'complete', 'finish', 'done']
        if any(keyword in message_lower for keyword in task_related_keywords):
            # If it's task-related but unclear, return UNKNOWN
            return {
                "intent": "UNKNOWN",
                "params": {}
            }

        # If no clear intent detected
        return {
            "intent": "UNKNOWN",
            "params": {}
        }

    def _extract_task_id(self, message: str) -> str:
        """
        Extract task ID from message using patterns like "task 1", "number 2", etc.
        """
        # Look for patterns like "task 1", "number 2", "#3", etc.
        patterns = [
            r'task\s+#?(\d+)',
            r'number\s+(\d+)',
            r'#(\d+)',
            r'no\.?\s*(\d+)',
            r'the\s+(\d+)(?:st|nd|rd|th)\s+(?:task|one)',
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1)

        # If no specific number found, return empty string
        return ""

    def process_message(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Process a user message and return AI response with tool calls
        """
        # Detect intent
        intent_result = self.detect_intent(message)
        intent = intent_result["intent"]
        params = intent_result["params"]

        tool_calls = []
        ai_response = ""

        # Handle the specific intents as per the specification
        if intent == "GREETING":
            ai_response = "Hello! 👋 I can help you manage your tasks.\nTry:\n- Add a task to buy groceries\n- List my tasks\n- Update task 1\n- Delete task 2"
            return {
                "response": ai_response,
                "tool_calls": []
            }

        elif intent == "ADD_TASK":
            title = params.get("title", "").strip()

            if not title:
                # Information is missing, ask the user following the specification
                ai_response = "Sure 🙂 What task would you like to add?"
                return {
                    "response": ai_response,
                    "tool_calls": []
                }
            else:
                # Add user_id to parameters
                params["user_id"] = user_id
                params["description"] = ""  # Add description parameter

                try:
                    # Call the add_task tool
                    result = self.tools["add_task"](**params)

                    tool_calls.append({
                        "tool_name": "add_task",
                        "input": params,
                        "result": result,
                        "status": "success"
                    })

                    ai_response = f"✅ Task added: {title}"

                except Exception as e:
                    # Never return backend or technical errors
                    tool_calls.append({
                        "tool_name": "add_task",
                        "input": params,
                        "result": {"error": str(e)},
                        "status": "error"
                    })
                    ai_response = f"Something went wrong adding your task. Please try again."

        elif intent == "LIST_TASKS":
            # Add user_id to parameters
            params["user_id"] = user_id

            try:
                # Call the list_tasks tool
                result = self.tools["list_tasks"](**params)

                tool_calls.append({
                    "tool_name": "list_tasks",
                    "input": params,
                    "result": result,
                    "status": "success"
                })

                ai_response = "Showing your current tasks 📋"

            except Exception as e:
                # Never return backend or technical errors
                tool_calls.append({
                    "tool_name": "list_tasks",
                    "input": params,
                    "result": {"error": str(e)},
                    "status": "error"
                })
                ai_response = "Something went wrong retrieving your tasks. Please try again."

        elif intent == "COMPLETE_TASK":
            task_id = params.get("task_id", "")

            if not task_id:
                # Information is missing, ask the user following the specification
                ai_response = "Which task number should I complete?"
                return {
                    "response": ai_response,
                    "tool_calls": []
                }
            else:
                # Add user_id to parameters
                params["user_id"] = user_id
                params["task_id"] = task_id

                try:
                    # Call the complete_task tool
                    result = self.tools["complete_task"](**params)

                    tool_calls.append({
                        "tool_name": "complete_task",
                        "input": params,
                        "result": result,
                        "status": "success"
                    })

                    ai_response = f"✅ Task marked as completed."

                except Exception as e:
                    # Never return backend or technical errors
                    tool_calls.append({
                        "tool_name": "complete_task",
                        "input": params,
                        "result": {"error": str(e)},
                        "status": "error"
                    })
                    ai_response = "Something went wrong completing that task. Please try again."

        elif intent == "DELETE_TASK":
            task_id = params.get("task_id", "")

            if not task_id:
                # Information is missing, ask the user following the specification
                ai_response = "Which task number should I delete?"
                return {
                    "response": ai_response,
                    "tool_calls": []
                }
            else:
                # Add user_id to parameters
                params["user_id"] = user_id
                params["task_id"] = task_id

                try:
                    # Call the delete_task tool
                    result = self.tools["delete_task"](**params)

                    tool_calls.append({
                        "tool_name": "delete_task",
                        "input": params,
                        "result": result,
                        "status": "success"
                    })

                    ai_response = f"🗑️ Task deleted."

                except Exception as e:
                    # Never return backend or technical errors
                    tool_calls.append({
                        "tool_name": "delete_task",
                        "input": params,
                        "result": {"error": str(e)},
                        "status": "error"
                    })
                    ai_response = "Something went wrong deleting that task. Please try again."

        elif intent == "UPDATE_TASK":
            task_id = params.get("task_id", "")
            new_content = params.get("new_content", "")

            if not task_id:
                # Information is missing, ask the user following the specification
                ai_response = "Which task number should I update?"
                return {
                    "response": ai_response,
                    "tool_calls": []
                }
            elif not new_content:
                # Information is missing, ask the user following the specification
                ai_response = f"What should I change task {task_id} to?"
                return {
                    "response": ai_response,
                    "tool_calls": []
                }
            else:
                # Add user_id to parameters
                params["user_id"] = user_id

                try:
                    # Call the update_task tool
                    result = self.tools["update_task"](**params)

                    tool_calls.append({
                        "tool_name": "update_task",
                        "input": params,
                        "result": result,
                        "status": "success"
                    })

                    ai_response = f"✏️ Task updated successfully."

                except Exception as e:
                    # Never return backend or technical errors
                    tool_calls.append({
                        "tool_name": "update_task",
                        "input": params,
                        "result": {"error": str(e)},
                        "status": "error"
                    })
                    ai_response = "Something went wrong updating that task. Please try again."

        elif intent == "UNKNOWN":
            # Follow the specification: Never say "Sorry, I couldn't process that request"
            # Instead, guide the user if input is unclear
            ai_response = "I didn't quite get that 😅\nYou can say:\n- Add a task\n- List tasks\n- Update a task\n- Delete a task"
        else:
            # For any other unexpected intent
            ai_response = "I didn't quite get that 😅\nYou can say:\n- Add a task\n- List tasks\n- Update a task\n- Delete a task"

        return {
            "response": ai_response,
            "tool_calls": tool_calls
        }
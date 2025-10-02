from app.models.v1.chat.llm_chat_schema import (
    CompletionMessageSchema,
    ChatMessageSchema,
    LlmConfig
)

from app.core.exceptions import (
    BadRequest
)

from typing import List, Iterator
import ollama
import json


class OllamaService:
    @staticmethod
    def is_model_available(model_name, support_structured_output:bool = False):
        try:
            ollama.show(model_name)
        except ollama.ResponseError:
            raise BadRequest("Model name not available")
        if support_structured_output:
            if 'qwen' not in model_name and 'llama' not in model_name:
                raise BadRequest(f"{model_name} is not designed for structured output")

    @staticmethod
    def get_model_list():
        return ollama.list().__dict__
    
    @staticmethod
    def validate_format_structure(structured_format: dict):
        """
        Validate structured output format like this
        {
            'type': 'object',
            'properties': {
                'animal_name': {'type': 'string'},
                'ordo': {'type': 'string'},
                'family': {'type': 'string'},
                'scientific_name': {'type': 'string'}
            },
            'required': ['animal_name', 'ordo', 'family', 'scientific_name']
        }
        """
        if 'type' not in structured_format.keys():
            raise ValueError("'type' key expected")
        
        if 'properties' not in structured_format.keys():
            raise ValueError("'properties' key expected")
        
        if 'required' not in structured_format.keys():
            raise ValueError("'required' key expected")
        
        if type(structured_format['type']) is not str:
            raise BadRequest("The value in 'type' key should be string")

        if type(structured_format['properties']) is not dict:
            raise BadRequest("The value in 'properties' key should be dictionary")
        
        if type(structured_format['required']) is not list:
            raise BadRequest("The value in 'required' key should be list")
        
        for item in structured_format['required']:
            if item not in structured_format['properties'].keys():
                raise ValueError(f"Required item '{item}' does not exist in properties")
    
    @staticmethod
    def generate_structured_output(structure_prompt):
        prompt = f"""
        Change this data structure into structured ollama structured output json format

        {structure_prompt}
        """

        example_output = """
        Example output :
        {
            "type": "object",
            "properties": {
            "name": {
                "type": "string"
            },
            "capital": {
                "type": "string"
            },
            "languages": {
                "type": "array",
                "items": {
                "type": "string"
                }
            }
            },
            "required": [
            "name",
            "capital", 
            "languages"
            ]
        }
        """

        SYSTEM_PROMPT = """
            You are a structured input converter to json format. 
            Just write the response in Json, no openning!
        """

        message_list = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": 'user',
                "content": prompt + example_output
            }
        ]

        result = ollama.chat(
            model='llama3.2',
            messages=message_list,
            options={
                "temperature": 0.2
            }
        )

        content = result.message.content.replace(
            "```json", ""
        ).replace("```","").strip()

        content = json.loads(content)

        return content

    @staticmethod
    def chat_return_dict(result: ollama.ChatResponse):
        message = result.message.content
        if "<think>" in message:
            message = message.split("</think>")[-1].strip()
            
        returned_dict = {
            "model": result.model,
            "done": result.done,
            "done_reason": result.done_reason,
            "usage": {
                "input_token_count": result.prompt_eval_count,
                "output_token_count": result.eval_count,
            },            
            "messages": {
                "role": result.message.role,
                "message": message,
                "images": result.message.images,
                "tool_calls": result.message.tool_calls
            }
        }
        return returned_dict
    
    @staticmethod
    def chat_structured_return_dict(result: ollama.ChatResponse):
        json_clean = result.message.content.replace("```json", "")
        json_clean = json_clean.replace("```", "").strip()
        returned_dict = {
            "model": result.model,
            "done": result.done,
            "done_reason": result.done_reason,
            "usage": {
                "input_token_count": result.prompt_eval_count,
                "output_token_count": result.eval_count,
            },            
            "messages": {
                "role": result.message.role,
                "message": result.message.content,
                "images": result.message.images,
                "tool_calls": result.message.tool_calls
            },
            "parsed": json.loads(json_clean)
        }
        return returned_dict

    @staticmethod
    def chat_return_dict_stream(result: Iterator[ollama.ChatResponse]):
        for item in result:
            returned_dict = {
                "model": item.model,
                "done": item.done,
                "done_reason": item.done_reason,
                "usage": {
                    "input_token_count": item.prompt_eval_count,
                    "output_token_count": item.eval_count,
                },                
                "messages": {
                    "role": item.message.role,
                    "message": item.message.content,
                    "images": item.message.images,
                    "tool_calls": item.message.tool_calls
                }
            }
            yield json.dumps(returned_dict) + "\n"

    @staticmethod
    def completion_return_dict(result: ollama.GenerateResponse):
        returned_dict = {
            "model": result.model,
            "done": result.done,
            "done_reason": result.done_reason,
            "usage": {
                "input_token_count": result.prompt_eval_count,
                "output_token_count": result.eval_count,
            },
            "response": result.response 
        }
        return returned_dict
    
    @staticmethod
    def completion_return_dict_stream(result: Iterator[ollama.GenerateResponse]):
        for item in result:
            returned_dict = {
                "model": item.model,
                "done": item.done,
                "done_reason": item.done_reason,
                "usage": {
                    "input_token_count": item.prompt_eval_count,
                    "output_token_count": item.eval_count,
                },
                "response": item.response 
            }
            yield json.dumps(returned_dict) + "\n"

    @staticmethod
    def chat_model(
        model_name: str,
        system_instruction: str,
        config: LlmConfig,
        messages: List[ChatMessageSchema],
        context_length: int = 4096
    ):
        OllamaService.is_model_available(model_name)
        messages_dict = [{
            "role": "system",
            "content": system_instruction
        }]

        messages_dict += [item.__dict__ for item in messages]
        result = ollama.chat(
            model=model_name,
            messages=messages_dict,
            options={
                "temperature": config.temperature,
                "top_k": config.top_k,
                "top_p": config.top_p,
                "num_ctx": context_length
            }
        )

        return result

    @staticmethod
    def chat_model_stream(
        model_name: str,
        system_instruction: str,
        config: LlmConfig,
        messages: List[ChatMessageSchema]
    ):
        OllamaService.is_model_available(model_name)
        messages_dict = [{
            "role": "system",
            "content": system_instruction
        }]

        messages_dict += [item.__dict__ for item in messages]
        result = ollama.chat(
            model=model_name,
            messages=messages_dict,
            options={
                "temperature": config.temperature,
                "top_k": config.top_k,
                "top_p": config.top_p
            },
            stream=True
        )

        return result
    
    @staticmethod
    def chat_model_structured_output(
        model_name: str,
        system_instruction: str,
        config: LlmConfig,
        messages: List[ChatMessageSchema],
        format: dict
    ):
        OllamaService.validate_format_structure(format)

        OllamaService.is_model_available(model_name, support_structured_output=True)
        messages_dict = [{
            "role": "system",
            "content": system_instruction
        }]

        messages_dict += [item.__dict__ for item in messages]
        result = ollama.chat(
            model=model_name,
            messages=messages_dict,
            options={
                "temperature": config.temperature,
                "top_k": config.top_k,
                "top_p": config.top_p
            },
            format=format
        )

        return result

    @staticmethod
    def chat_model_structured_output_custom(
        model_name: str,
        system_instruction: str,
        config: LlmConfig,
        messages: List[ChatMessageSchema],
        format: str
    ):
        OllamaService.is_model_available(model_name, support_structured_output=True)

        format = OllamaService.generate_structured_output(
            format
        )

        messages_dict = [{
            "role": "system",
            "content": system_instruction
        }]

        messages_dict += [item.__dict__ for item in messages]
        result = ollama.chat(
            model=model_name,
            messages=messages_dict,
            options={
                "temperature": config.temperature,
                "top_k": config.top_k,
                "top_p": config.top_p
            },
            format=format
        )

        return result

    @staticmethod
    def completion_model(
        model_name: str,
        system_instruction: str,
        message: CompletionMessageSchema,
        config: LlmConfig,
    ):
        OllamaService.is_model_available(model_name)
        result = ollama.generate(
            model=model_name,
            system=system_instruction,
            prompt=message.prompt,
            options={
                "temperature": config.temperature,
                "top_k": config.top_k,
                "top_p": config.top_p
            }
        )

        return result

    @staticmethod
    def completion_model_stream(
        model_name: str,
        system_instruction: str,
        message: CompletionMessageSchema,
        config: LlmConfig
    ):
        OllamaService.is_model_available(model_name)
        result = ollama.generate(
            model=model_name,
            system=system_instruction,
            prompt=message.prompt,
            options={
                "temperature": config.temperature,
                "top_k": config.top_k,
                "top_p": config.top_p
            },
            stream=True
        )

        return result

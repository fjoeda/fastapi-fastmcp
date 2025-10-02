from pydantic import BaseModel


class ChatMessageSchema(BaseModel):
    role: str
    content: str


class CompletionMessageSchema(BaseModel):
    prompt: str


class LlmConfig(BaseModel):
    temperature: float = 0.8
    top_k: float = 20
    top_p: float = 0.9


class ChatModelSchema(BaseModel):
    model_name: str
    system_instruction: str
    messages: list[ChatMessageSchema]
    config: LlmConfig


class CompletionModelSchema(BaseModel):
    model_name: str
    system_instruction: str
    prompt: CompletionMessageSchema
    config: LlmConfig


class StructuredOutputFixedSchema(BaseModel):
    model_name: str
    system_instruction: str
    messages: list[ChatMessageSchema]
    config: LlmConfig
    structured_format: dict = {"type": "object", "properties": {}, "required": []}


class StructuredOutputFlexibleSchema(BaseModel):
    model_name: str
    system_instruction: str
    messages: list[ChatMessageSchema]
    config: LlmConfig
    structured_format: str


class QuestionSchema(BaseModel):
    question: str

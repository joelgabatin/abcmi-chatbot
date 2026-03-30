from typing import Any, Text, Dict, List, Type
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=False
)
class LowercaseNormalizer(GraphComponent):
    """
    Custom NLU pipeline component that lowercases all user messages
    before tokenization and entity extraction.

    This makes entity extraction case-insensitive without requiring
    multiple case variants in training data.
    """

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> "LowercaseNormalizer":
        return cls()

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get("text")
            if text:
                message.set("text", text.lower())
        return messages

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        for message in training_data.training_examples:
            text = message.get("text")
            if text:
                message.set("text", text.lower())
        return training_data

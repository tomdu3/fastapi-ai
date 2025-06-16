from abc import ABC, abstractmethod

class AIPlatform(ABC):
    """
    Abstract base class for AI platforms.
    """

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """
        Method to generate a chat response based on the provided prompt.
        
        :param prompt: The input text for the chat.
        :return: The generated response text.
        """
        pass
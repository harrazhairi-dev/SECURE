from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def analyze(self, components):
        """Analyze components and return security assessment"""
        pass 
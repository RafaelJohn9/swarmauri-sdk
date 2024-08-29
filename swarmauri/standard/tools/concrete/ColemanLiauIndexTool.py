import re
from typing import Any, Dict, List, Literal
from swarmauri.standard.tools.base.ToolBase import ToolBase
from swarmauri.standard.tools.concrete.Parameter import Parameter

class ColemanLiauIndexTool(ToolBase):
    """
    A tool for calculating the Coleman-Liau Index (CLI).

    Attributes:
        version (str): The version of the tool.
        name (str): The name of the tool.
        type (Literal["ColemanLiauIndexTool"]): The type of the tool.
        description (str): A brief description of what the tool does.
        parameters (List[Parameter]): The parameters for configuring the tool.
    """
    version: str = "0.1.dev1"
    name: str = "ColemanLiauIndexTool"
    type: Literal["ColemanLiauIndexTool"] = "ColemanLiauIndexTool"
    description: str = "Calculates the Coleman-Liau Index (CLI) for a given text."
    parameters: List[Parameter] = [
        Parameter(
            name="input_text",
            type="string",
            description="The input text for which to calculate the CLI.",
            required=True
        )
    ]

    def __call__(self, data: Dict[str, Any]) -> float:
        """
        Executes the CLI tool and returns the readability score.

        Coleman-Liau Index formula:
        CLI = 0.0588 * (characters/words * 100) - 0.296 * (sentences/words * 100) - 15.8
        
        Parameters:
            data (Dict[str, Any]): The input data containing "input_text".
        
        Returns:
            float: The Coleman-Liau Index.

        Raises:
            ValueError: If the input data is invalid.
        """
        if self.validate_input(data):
            text = data['input_text']
            num_sentences = self.count_sentences(text)
            num_words = self.count_words(text)
            num_characters = self.count_characters(text)
            if num_sentences == 0 or num_words == 0:
                return 0.0
            L = (num_characters / num_words) * 100  # Average number of letters per 100 words
            S = (num_sentences / num_words) * 100  # Average number of sentences per 100 words
            cli_score = 0.0588 * L - 0.296 * S - 15.8
            return cli_score
        else:
            raise ValueError("Invalid input for ColemanLiauIndexTool.")

    def count_sentences(self, text: str) -> int:
        """
        Counts the number of sentences in the text.
        
        Parameters:
            text (str): The input text.
        
        Returns:
            int: The number of sentences in the text.
        """
        sentence_endings = re.compile(r'[.!?]')
        sentences = sentence_endings.split(text)
        return len([s for s in sentences if s.strip()])  # Count non-empty sentences

    def count_words(self, text: str) -> int:
        """
        Counts the number of words in the text.
        
        Parameters:
            text (str): The input text.
        
        Returns:
            int: The number of words in the text.
        """
        words = re.findall(r'\b\w+\b', text)
        return len(words)

    def count_characters(self, text: str) -> int:
        """
        Counts the number of characters in the text.
        
        Parameters:
            text (str): The input text.
        
        Returns:
            int: The number of characters in the text.
        """
        return len(text) - text.count(' ')  # Count characters excluding spaces
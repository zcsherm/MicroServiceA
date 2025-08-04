class Font:
    def __init__(self, name: str, letterChart: dict):
        """
        Args:
            name (str): Name of the font
            letterChart (dict): Dictionary mapping letters to 2D array objects
        """
        self.name = name
        self.letters = letterChart

    def getLetterChart(self, char: str):
        """Returns the 2D array for the given letter, or none if not found

        Args:
            char (str): The letter for which we want a grid
        """
        return self.letters.get(char)
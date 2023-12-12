"""Project Model"""


class Project:
    """Project Class"""

    def __init__(self, name) -> None:
        self.name = name

    def get_name(self):
        """Get name"""
        return self.name

"""
Storage Module
"""

import json


class Storage:
    """
    A class to manage the storage of blog posts in a JSON file.

    Attributes:
        path (str): Path to the JSON file.
    """

    def __init__(self, path: str):
        """
        Initialize the Storage with the file path.

        Args:
            path (str): Path to the JSON file.
        """
        self.path = path

    def load_posts(self) -> list:
        """
        Load blog posts from the JSON file.

        Returns:
            list: List of blog posts.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file is missing or unreadable, return an empty list and create the file.
            self.save_posts([])  # Initializes the file if it does not exist.
            return []

    def save_posts(self, posts: list[dict]) -> None:
        """
        Save the current list of blog posts to the JSON file.

        Args:
            posts (list[dict]): List of blog posts to save.
        """
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(posts, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error: Unable to write to the file '{self.path}: {e}")

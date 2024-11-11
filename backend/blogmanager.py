"""
Blog Manager Module
"""

from datetime import datetime
from storage.storage import Storage


class BlogManager:
    """
    Blog Manager class to handle post management operations.

    Attributes:
        FIELDS (set): Required fields for a blog post.
    """
    FIELDS = {'title', 'content', 'author'}

    def __init__(self, storage: Storage):
        """
        Initialize the BlogManager.

        Args:
            storage (Storage): An instance of Storage for handling data persistence.
        """
        self.storage = storage

    @staticmethod
    def _generate_id(posts: list[dict]) -> int:
        """
        Generate a unique ID for a new post.

        Args:
            posts (list[dict]): List of existing posts.

        Returns:
            int: A unique ID.
        """
        return max(post['id'] for post in posts) + 1 if posts else 1

    @staticmethod
    def _format_datetime(iso_string):
        """Format datetime string to a readable format."""
        date = datetime.fromisoformat(iso_string)
        return date.strftime('%B %d, %Y, %I:%M %p')

    def get_all_posts(self) -> list[dict]:
        """
        Retrieve all posts.

        Returns:
            list[dict]: List of all posts.
        """
        posts = self.storage.load_posts()
        for post in posts:
            post['created_at'] = self._format_datetime(post['created_at'])
            if 'updated_at' in post:
                post['updated_at'] = self._format_datetime(post['updated_at'])
        return posts

    def get_post_by_id(self, post_id: int, posts=None) -> [dict]:
        """
        Retrieve a post by ID.

        Args:
            post_id (int): The ID of the post.
            posts (list, optional): List of posts to search in. Defaults to None.

        Returns:
        dict or None: The post data if found, otherwise None.
        """
        posts = posts or self.storage.load_posts()
        return next((post for post in posts if post['id'] == post_id), None)

    def validate_data(self, data):
        """
        Validate the fields in post data.

        Args:
            data (dict): Post data to validate.

        Returns:
            dict or None: Error message if validation fails, None otherwise.
        """
        missing_fields = [field for field in self.FIELDS if not data.get(field)]
        if missing_fields:
            return {"error": f"Missing fields: {', '.join(missing_fields)}"}
        return None

    def add_post(self, data: dict) -> dict:
        """
        Add a new post.

        Args:
            data (dict): Post data.

        Returns:
            dict: The newly created post data.
        """
        posts = self.storage.load_posts()
        data['id'] = BlogManager._generate_id(posts)
        data['created_at'] = datetime.utcnow().isoformat()
        posts.append(data)
        self.storage.save_posts(posts)
        return data

    def delete_post(self, post_id: int) -> bool:
        """
        Delete a post by ID.

        Args:
            post_id (int): The ID of the post to delete.

        Returns:
            bool: True if deleted, False if post not found.
        """
        posts = self.storage.load_posts()
        post = self.get_post_by_id(post_id, posts)
        if post:
            posts.remove(post)
            self.storage.save_posts(posts)
            return True
        return False

    def update_post(self, post_id: int, data: dict) -> [dict]:
        """
        Update an existing post by ID.

        Args:
            post_id (int): The ID of the post.
            data (dict): Data to update the post with.

        Returns:
            dict or None: Updated post data if successful, None otherwise.
        """
        posts = self.storage.load_posts()
        post = self.get_post_by_id(post_id, posts)
        if post:
            for key, value in data.items():
                if key in self.FIELDS:
                    post[key] = value
            post['updated_at'] = datetime.utcnow().isoformat()
            self.storage.save_posts(posts)
        return post

    def search_posts(self, query: dict) -> list[dict]:
        """
        Search posts based on query parameters.

        Args:
            query (dict): Search criteria.

        Returns:
            list[dict]: List of matching posts.
        """
        posts = self.storage.load_posts()
        return [post for post in posts if self._matches_query(post, query)]

    def _matches_query(self, post: dict, query: dict) -> bool:
        """
        Check if a post matches all the criteria in the query.

        Args:
            post (dict): Post data.
            query (dict): Query criteria.

        Returns:
            bool: True if all criteria match, False otherwise.
        """
        return all(str(post.get(field, '')).lower().find(str(value).lower()) != -1
                   for field, value in query.items() if field in self.FIELDS)

"""
Blog Manager Module for handling blog post creation, retrieval, updating, and deletion.
"""

from datetime import datetime, timezone
from storage.storage import Storage


class BlogManager:
    """
    Blog Manager class to handle blog post management operations.

    Attributes:
        REQUIRED_FIELDS (set): Fields that are required for a blog post.
        VALID_SORT_FIELDS (set): Fields that can be used to sort posts.
        VALID_DIRECTIONS (set): Valid directions for sorting posts (ascending or descending).
    """
    REQUIRED_FIELDS = {'title', 'content', 'author'}
    VALID_SORT_FIELDS = {'title', 'content', 'author', 'created', 'updated'}
    VALID_DIRECTIONS = {"asc", "desc"}

    def __init__(self, storage: Storage):
        """
        Initialize the BlogManager with a storage instance.

        Args:
            storage (Storage): An instance of Storage to handle data persistence.
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
        """
        Convert an ISO datetime string to 'YYYY-MM-DD' format.

        Args:
            iso_string (str): The ISO date string.

        Returns:
            str: Formatted date string in 'YYYY-MM-DD' format.
        """
        date = datetime.fromisoformat(iso_string)
        return date.strftime('%Y-%m-%d')

    def get_all_posts(self, sort: str = None, direction: str = 'asc') -> dict:
        """
        Retrieve all posts with optional sorting and display formatting.

        Args:
            sort (str): Field to sort by. Must be in VALID_SORT_FIELDS.
            direction (str): Sort direction, either 'asc' for ascending or 'desc' for descending.

        Returns:
            dict: A dictionary containing either:
                  - "posts" key with a list of posts if valid parameters are provided
                  - "error" key with a message if parameters are invalid
        """
        # Validate sorting parameters
        if sort and sort not in self.VALID_SORT_FIELDS:
            return {"error": f"Invalid sort field [{sort}]. "
                             f"Valid options are: {', '.join(self.VALID_SORT_FIELDS)}"}

        if direction not in self.VALID_DIRECTIONS:
            return {"error": f"Invalid sort direction [{direction}]. "
                             f"Valid options are: {', '.join(self.VALID_DIRECTIONS)}"}

        # Load posts from storage
        posts = self.storage.load_posts()

        # Apply sorting if a valid field is provided
        if sort:
            reverse = direction == 'desc'
            posts.sort(key=lambda post: post.get(sort, ''), reverse=reverse)

        # Format dates for display after sorting
        for post in posts:
            post['created'] = self._format_datetime(post.get('created', ""))
            if 'updated' in post:
                post['updated'] = self._format_datetime(post.get('updated', ""))
        # Return the list of posts in a dictionary for the API response
        return {"posts": posts}

    def get_post_by_id(self, post_id: int, posts=None) -> dict:
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
        missing_fields = [field for field in self.REQUIRED_FIELDS if not data.get(field)]
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
        data['created'] = datetime.now(timezone.utc).isoformat()
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

    def update_post(self, post_id: int, data: dict) -> dict:
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
                if key in self.REQUIRED_FIELDS:
                    post[key] = value
            post['updated'] = datetime.now(timezone.utc).isoformat()
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
        filtered_posts = [post for post in posts if self._matches_query(post, query)]
        # Format dates for display after filtering
        for post in filtered_posts:
            post['created'] = self._format_datetime(post.get('created', ""))
            if 'updated' in post:
                post['updated'] = self._format_datetime(post.get('updated', ""))
        return filtered_posts

    def _matches_query(self, post: dict, query: dict) -> bool:
        """
        Check if a post matches all the criteria in the query.

        Args:
            post (dict): Post data.
            query (dict): Query criteria.

        Returns:
            bool: True if all criteria match, False otherwise.
        """
        for field, search_value in query.items():
            if field not in self.REQUIRED_FIELDS:
                continue

            # Get post field value and search criteria,
            # both in lowercase for case-insensitive comparison
            post_value = str(post.get(field, '')).lower()
            search_value = str(search_value).lower()

            # If search value is not in post value, the post does not match the query
            if search_value not in post_value:
                return False

        return True

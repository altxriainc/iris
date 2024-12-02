# ## TemplateCache Class
# 
# This module implements a caching mechanism for templates. It stores rendered templates
# to speed up future rendering with the same template and context.
# 
# ### Features:
# - Generates a unique cache key for a template and its context.
# - Stores rendered templates in a specified cache directory.
# - Checks if a cached version exists and retrieves it if available.
# 
# ### Usage:
# - Initialize the class with an optional `cache_dir`.
# - Use `store` to save a rendered template.
# - Use `get` to retrieve a cached template if available.

import hashlib
import json
import os

class TemplateCache:
    """
    A simple cache manager for template rendering.
    
    Attributes:
        cache_dir (str): Directory to store cached templates.
    """
    
    def __init__(self, cache_dir=".cache"):
        """
        Initializes the cache with a specified directory.
        If the directory does not exist, it is created.

        Args:
            cache_dir (str): Path to the cache directory. Defaults to '.cache'.
        """
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _generate_cache_key(self, template_path, context):
        """
        Generates a unique MD5 hash as the cache key based on the template path and context.

        Args:
            template_path (str): Path to the template file.
            context (dict): Context dictionary used for rendering.

        Returns:
            str: MD5 hash representing the unique cache key.
        """
        key = f"{template_path}-{json.dumps(context, sort_keys=True)}"
        return hashlib.md5(key.encode()).hexdigest()

    def is_cached(self, template_path, context):
        """
        Checks if a cached version of the template exists.

        Args:
            template_path (str): Path to the template file.
            context (dict): Context dictionary used for rendering.

        Returns:
            bool: True if the cache exists, False otherwise.
        """
        key = self._generate_cache_key(template_path, context)
        return os.path.exists(os.path.join(self.cache_dir, key))

    def get(self, template_path, context):
        """
        Retrieves the cached template content.

        Args:
            template_path (str): Path to the template file.
            context (dict): Context dictionary used for rendering.

        Returns:
            str: Cached rendered template content.

        Raises:
            FileNotFoundError: If the cache file does not exist.
        """
        key = self._generate_cache_key(template_path, context)
        cache_path = os.path.join(self.cache_dir, key)
        if not os.path.exists(cache_path):
            raise FileNotFoundError(f"No cached template found for key: {key}")
        with open(cache_path, "r") as file:
            return file.read()

    def store(self, template_path, context, rendered_template):
        """
        Stores the rendered template in the cache.

        Args:
            template_path (str): Path to the template file.
            context (dict): Context dictionary used for rendering.
            rendered_template (str): The rendered template content to cache.
        """
        key = self._generate_cache_key(template_path, context)
        cache_path = os.path.join(self.cache_dir, key)
        with open(cache_path, "w") as file:
            file.write(rendered_template)

import os
from .parser import TemplateParser
from .cache import TemplateCache
from .exceptions import TemplateNotFoundException

class TemplateEngine:
    """
    A class to render templates with context injection and caching support.

    Attributes:
        template_dir (str): The directory containing the template files.
        parser (TemplateParser): The parser to handle template parsing.
        cache (TemplateCache): Optional cache for storing rendered templates.
    """

    def __init__(self, template_dir: str = None, cache_enabled=True):
        """
        Initializes the TemplateEngine.

        Args:
            template_dir (str): Path to the directory containing template files.
                               Defaults to a 'templates' folder in the current working directory.
            cache_enabled (bool): Enables or disables caching. Defaults to True.
        """
        self.template_dir = template_dir or os.path.join(os.getcwd(), "templates")
        self.parser = TemplateParser(self)  
        self.cache = TemplateCache() if cache_enabled else None

    def render(self, template_name: str, context: dict = None) -> str:
        """
        Renders a template file with the provided context.

        Args:
            template_name (str): The name of the template file to render.
            context (dict): A dictionary containing variables to inject into the template.
                            Defaults to an empty dictionary.

        Returns:
            str: The rendered template.

        Raises:
            TemplateNotFoundException: If the specified template file does not exist.

        Example:
            engine = TemplateEngine(template_dir="templates")
            output = engine.render("home.html", {"user": "Alice"})
            print(output)
        """
        context = context or {}
        template_path = os.path.join(self.template_dir, template_name)

        # Check if template is cached
        if self.cache and self.cache.is_cached(template_path, context):
            return self.cache.get(template_path, context)

        # Check if template file exists
        if not os.path.exists(template_path):
            raise TemplateNotFoundException(f"Template '{template_name}' not found.")

        # Load and parse the template
        with open(template_path, "r") as file:
            raw_template = file.read()

        rendered_template = self.parser.parse(raw_template, context)

        # Store in cache if caching is enabled
        if self.cache:
            self.cache.store(template_path, context, rendered_template)

        return rendered_template

    def render_string(self, template_string: str, context: dict) -> str:
        """
        Renders a template directly from a string with the provided context.

        Args:
            template_string (str): The raw template string to render.
            context (dict): A dictionary containing variables to inject into the template.

        Returns:
            str: The rendered template.

        Example:
            engine = TemplateEngine()
            output = engine.render_string("Hello, {{ user }}!", {"user": "Alice"})
            print(output)  # Output: "Hello, Alice!"
        """
        rendered_template = self.parser.parse(template_string, context)
        return rendered_template

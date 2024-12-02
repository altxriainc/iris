# ## Directives Class
#
# This module manages custom directives for template processing.
# Directives are user-defined handlers that can be registered and processed dynamically.
#
# ### Features:
# - Register custom directives with unique names.
# - Dynamically invoke handlers for registered directives.
# - Maintain a clean and extensible directive system.

class Directives:
    """
    Manages custom directives for template processing.

    Attributes:
        directives (dict): A dictionary mapping directive names to their respective handlers.
    """

    def __init__(self):
        """
        Initializes the Directives class with an empty dictionary to store directive handlers.
        """
        self.directives = {}

    def register(self, name, handler):
        """
        Registers a custom directive with its associated handler.

        Args:
            name (str): The unique name of the directive.
            handler (callable): A function or callable object to handle the directive.

        Example:
            directives = Directives()
            directives.register("example", lambda args, context: f"Handled {args}")
        """
        self.directives[name] = handler

    def process(self, name, args, context):
        """
        Processes a directive by invoking its registered handler.

        Args:
            name (str): The name of the directive to process.
            args (list): Arguments passed to the directive.
            context (dict): The context in which the directive is executed.

        Returns:
            The result of the directive handler.

        Raises:
            ValueError: If the directive is not registered.

        Example:
            directives = Directives()
            directives.register("example", lambda args, context: f"Handled {args}")
            result = directives.process("example", ["arg1", "arg2"], {"key": "value"})
            print(result)  # Output: "Handled ['arg1', 'arg2']"
        """
        if name not in self.directives:
            raise ValueError(f"Directive {name} is not registered.")
        return self.directives[name](args, context)

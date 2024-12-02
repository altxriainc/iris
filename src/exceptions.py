# ## Template Engine Exceptions
#
# This module defines custom exceptions used throughout the template engine.
# These exceptions improve error handling and readability when processing templates.

class TemplateNotFoundException(Exception):
    """
    Raised when a specified template file cannot be found.
    
    Example:
        raise TemplateNotFoundException("Template 'home.html' not found.")
    """
    pass


class TemplateSyntaxError(Exception):
    """
    Raised when a syntax error is detected in the template.
    
    Example:
        raise TemplateSyntaxError("Unexpected token in template.")
    """
    pass


class BreakLoop(Exception):
    """
    Raised internally to handle the `@break` directive in loops.
    
    Example:
        raise BreakLoop  # Stops the current loop iteration and exits the loop.
    """
    pass


class ContinueLoop(Exception):
    """
    Raised internally to handle the `@continue` directive in loops.
    
    Example:
        raise ContinueLoop  # Skips the current loop iteration and continues to the next.
    """
    pass

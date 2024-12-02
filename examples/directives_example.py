# ## Directives Example for Using TemplateEngine
# 
# This script demonstrates how to use advanced directives such as loops, conditionals,
# and other features provided by the `TemplateEngine`.
# Ensure the `templates` directory and `pages/home2.html` exist for this example to work.

import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.engine import TemplateEngine

# Initialize the TemplateEngine with the templates directory
engine = TemplateEngine(template_dir="./templates", cache_enabled=False)

# Define a complex context to demonstrate advanced directives
context = {
    "user": {"name": "Alice"},
    "orders": [],  # Empty orders list
    "items": ["Item1", "Skip", "Item2"],  # Items for a loop
    "status": "success",  # Example status for a switch-case
}

# Render the template with the context
output = engine.render("pages/home2.html", context)

# Print the rendered output
print(output)

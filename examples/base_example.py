# ## Base Example for Using TemplateEngine
# 
# This script demonstrates how to render a basic template using the `TemplateEngine` class.
# It includes setting up the context and rendering a single template file.
# Ensure the `templates` directory and `pages/home.html` exist for this example to work.

import sys
import os

# Add the project root directory to sys.path to allow importing from `src`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.engine import TemplateEngine

# Initialize the TemplateEngine with the templates directory
engine = TemplateEngine(template_dir="./templates", cache_enabled=False)

# Define the context to pass to the template
context = {
    "user": {"name": "Alice", "is_admin": True},
}

# Render the template with the context
output = engine.render("pages/home.html", context)

# Print the rendered output
print(output)

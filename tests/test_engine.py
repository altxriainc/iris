import unittest
import os
import sys

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from src.engine import TemplateEngine

class TestTemplateEngine(unittest.TestCase):
    def setUp(self):
        # Initialize the TemplateEngine with the template directory
        self.engine = TemplateEngine(template_dir="./templates")
        self.context = {
            "user": {"name": "Alice"},
            "orders": [],
            "items": ["Item1", "Skip", "Item2"],
            "status": "success"
        }

    def normalize_whitespace(self, s):
        # Remove leading and trailing whitespace from each line
        lines = [line.strip() for line in s.strip().splitlines() if line.strip()]
        # Join the lines into a single string
        return '\n'.join(lines)

    def test_isset_directive(self):
        template = '''
        @isset('user')
            <p>User is set: {{ user['name'] }}</p>
        @endisset
        '''
        expected_output = '''
        <p>User is set: Alice</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_empty_directive(self):
        template = '''
        @empty('orders')
            <p>No orders found.</p>
        @endempty
        '''
        expected_output = '''
        <p>No orders found.</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_for_loop(self):
        template = '''
        @for
        i in range(3)
            <p>For Loop Iteration: {{ i }}</p>
            @if(i == 1)
                @continue
            @endif
            <p>After possible continue</p>
        @endfor
        '''
        expected_output = '''
        <p>For Loop Iteration: 0</p>
        <p>After possible continue</p>
        <p>For Loop Iteration: 2</p>
        <p>After possible continue</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_foreach_loop(self):
        template = '''
        @foreach
        item in items
            <p>Item: {{ item }}</p>
            @if(item == 'Skip')
                @continue
            @endif
            <p>Processed Item: {{ item }}</p>
        @endforeach
        '''
        expected_output = '''
        <p>Item: Item1</p>
        <p>Processed Item: Item1</p>
        <p>Item: Item2</p>
        <p>Processed Item: Item2</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_switch_directive(self):
        template = '''
        @switch(status)
            @case('success')
                <p>Operation was successful.</p>
            @break
            @case('error')
                <p>There was an error.</p>
            @break
            @default
                <p>Status unknown.</p>
        @endswitch
        '''
        expected_output = '''
        <p>Operation was successful.</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_comments(self):
        template = '''
        {{-- This is a comment and should not appear in the output --}}
        <p>Visible content.</p>
        '''
        expected_output = '''
        <p>Visible content.</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_python_block(self):
        template = '''
        @python
        total = len(items)
        @endpython
        <p>Total items: {{ total }}</p>
        '''
        expected_output = '''
        <p>Total items: 3</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

    def test_include_directive(self):
        # Create a temporary included template
        include_template_path = os.path.join(self.engine.template_dir, 'included.html')
        with open(include_template_path, 'w') as f:
            f.write('<p>Included Content: {{ user["name"] }}</p>')

        template = '''
        @include('included.html')
        '''
        expected_output = '''
        <p>Included Content: Alice</p>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

        # Clean up the temporary included template
        os.remove(include_template_path)

    def test_extends_and_sections(self):
        # Create a temporary parent template
        parent_template_path = os.path.join(self.engine.template_dir, 'parent.html')
        with open(parent_template_path, 'w') as f:
            f.write('''
            <html>
                <head>
                    <title>@yield('title')</title>
                </head>
                <body>
                    @yield('content')
                </body>
            </html>
            ''')

        template = '''
        @extends('parent.html')
        @section('title', 'Page Title')
        @section('content')
            <p>Page Content</p>
        @endsection
        '''
        expected_output = '''
        <html>
            <head>
                <title>Page Title</title>
            </head>
            <body>
                <p>Page Content</p>
            </body>
        </html>
        '''
        output = self.engine.render_string(template, self.context)
        self.assertEqual(self.normalize_whitespace(output), self.normalize_whitespace(expected_output))

        # Clean up the temporary parent template
        os.remove(parent_template_path)

if __name__ == '__main__':
    unittest.main()

import os
import re
import ast
from .exceptions import BreakLoop, ContinueLoop, TemplateNotFoundException

class DirectiveHandlerBase:
    def _safe_eval(self, expr, context):
        allowed_nodes = (
            ast.Expression,
            ast.Call,
            ast.Name,
            ast.Load,
            ast.Constant,
            ast.Dict,
            ast.List,
            ast.Tuple,
            ast.Subscript,
            ast.Index,
            ast.Slice,
            ast.Attribute,
            ast.BinOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Mod,
            ast.Pow,
            ast.Compare,
            ast.Eq,
            ast.NotEq,
            ast.Lt,
            ast.LtE,
            ast.Gt,
            ast.GtE,
            ast.Is,
            ast.IsNot,
            ast.In,
            ast.NotIn,
            ast.BoolOp,
            ast.And,
            ast.Or,
            ast.UnaryOp,
            ast.Not,
            ast.USub,
            ast.UAdd,
            ast.IfExp,
        )

        expr = expr.strip()
        try:
            node = ast.parse(expr, mode='eval')

            for subnode in ast.walk(node):
                if not isinstance(subnode, allowed_nodes):
                    raise ValueError(f"Disallowed expression: {expr}")

            code = compile(node, '<string>', 'eval')
            return eval(code, {}, context)
        except Exception as e:
            raise ValueError(f"Error evaluating expression '{expr}': {e}")

    def _safe_exec(self, code_str, context):
        allowed_nodes = (
            ast.Module,
            ast.Expr,
            ast.Assign,
            ast.AugAssign,
            ast.Name,
            ast.Load,
            ast.Store,
            ast.Constant,
            ast.Dict,
            ast.List,
            ast.Tuple,
            ast.Subscript,
            ast.Index,
            ast.Slice,
            ast.Attribute,
            ast.BinOp,
            ast.Add,
            ast.Sub,
            ast.Mult,
            ast.Div,
            ast.Mod,
            ast.Pow,
            ast.Compare,
            ast.Eq,
            ast.NotEq,
            ast.Lt,
            ast.LtE,
            ast.Gt,
            ast.GtE,
            ast.Is,
            ast.IsNot,
            ast.In,
            ast.NotIn,
            ast.BoolOp,
            ast.And,
            ast.Or,
            ast.UnaryOp,
            ast.Not,
            ast.USub,
            ast.UAdd,
            ast.If,
            ast.For,
            ast.While,
            ast.Break,
            ast.Continue,
            ast.Pass,
            ast.FunctionDef,
            ast.Return,
            ast.Call,
            ast.arguments,
            ast.arg,
            ast.keyword,
        )

        code_str = code_str.strip()
        try:
            node = ast.parse(code_str, mode='exec')

            for subnode in ast.walk(node):
                if not isinstance(subnode, allowed_nodes):
                    raise ValueError(f"Disallowed statement in @python block: {ast.dump(subnode)}")

            code = compile(node, '<string>', 'exec')

            # Use context for both globals and locals
            exec(code, context, context)
        except Exception as e:
            raise ValueError(f"Error executing code in @python block: {e}")

class ExtendsHandler(DirectiveHandlerBase):
    def __init__(self, engine):
        self.engine = engine

    def process_extends(self, template, context, parser):
        extends_pattern = r"@extends\(\s*(['\"])(.*?)\1\s*\)"
        match = re.search(extends_pattern, template)

        if match:
            parent_template_name = match.group(2)
            parent_template_path = os.path.join(self.engine.template_dir, parent_template_name)
            if not os.path.exists(parent_template_path):
                raise TemplateNotFoundException(f"Parent template '{parent_template_name}' not found.")

            with open(parent_template_path, "r") as file:
                parent_template = file.read()

            # Remove @extends directive from child template
            template = re.sub(extends_pattern, '', template)

            # Extract sections from child template and get modified template
            sections, template_after_removal = self.extract_sections(template)

            # Include any remaining content in a default 'content' section
            if template_after_removal.strip():
                sections.setdefault('content', '')
                sections['content'] += '\n' + template_after_removal.strip()

            # Replace @yield directives in parent content with child sections
            combined_template = self.replace_yields(parent_template, sections, context, parser)

            return combined_template
        else:
            return template

    def extract_sections(self, template):
        sections = {}

        section_pattern = r"@section\(\s*(['\"])(?P<name>.*?)\1\s*(?:,\s*\1(?P<content_inline>.*?)\1\s*\)|\)\s*(?P<content_block>[\s\S]*?)@endsection)"

        matches = re.finditer(section_pattern, template, flags=re.DOTALL)

        for match in matches:
            name = match.group('name').strip()
            content = match.group('content_inline') or match.group('content_block') or ''
            sections[name] = content.strip()

        # Remove all sections from the template
        template = re.sub(section_pattern, '', template, flags=re.DOTALL)

        return sections, template

    def replace_yields(self, template, sections, context, parser):
        yield_pattern = r"@yield\(['\"](.*?)['\"](?:\s*,\s*['\"]([\s\S]*?)['\"])?\)"

        def yield_replacer(match):
            name = match.group(1).strip()
            default = match.group(2).strip() if match.group(2) else ''
            content = sections.get(name, default)
            if content:
                # Process the section content for includes and directives
                content = parser.process_template(content, context)
            return content

        template = re.sub(yield_pattern, yield_replacer, template, flags=re.DOTALL)
        return template

class IncludeHandler(DirectiveHandlerBase):
    def __init__(self, engine):
        self.engine = engine

    def process_includes(self, template, context, parser):
        # Existing @include processing
        include_pattern = r"@include\(['\"](.*?)['\"]\)"

        def include_replacer(match):
            included_template_name = match.group(1)
            return self.get_included_template(included_template_name, context, parser)

        template = re.sub(include_pattern, include_replacer, template, flags=re.DOTALL)

        # Add @includeIf processing
        include_if_pattern = r"@includeIf\((.*?)\)"

        def include_if_replacer(match):
            expression = match.group(1)
            # The expression should be something like "'template.html', condition"
            try:
                args = [arg.strip() for arg in expression.split(',')]
                template_name = self._safe_eval(args[0], context)
                condition = self._safe_eval(args[1], context)
                if condition:
                    return self.get_included_template(template_name, context, parser)
                else:
                    return ''
            except Exception as e:
                raise ValueError(f"Error in @includeIf: {e}")

        return re.sub(include_if_pattern, include_if_replacer, template, flags=re.DOTALL)

    def get_included_template(self, template_name, context, parser):
        included_template_path = os.path.join(self.engine.template_dir, template_name)
        if not os.path.exists(included_template_path):
            raise TemplateNotFoundException(f"Included template '{template_name}' not found.")
        with open(included_template_path, "r") as file:
            included_template = file.read()
        # Process the included template
        return parser.parse(included_template, context)

class CommentHandler:
    def process_comments(self, template):
        # Pattern to match comments like {{-- Comment --}}
        comment_pattern = r"\{\{--[\s\S]*?--\}\}"
        return re.sub(comment_pattern, '', template)

class PythonHandler(DirectiveHandlerBase):
    def process_python(self, template, context):
        python_pattern = r"@python(.*?)@endpython"

        def python_replacer(match):
            code = match.group(1).strip()
            self._safe_exec(code, context)
            return ''

        return re.sub(python_pattern, python_replacer, template, flags=re.DOTALL)

class VariableHandler(DirectiveHandlerBase):
    def process_variables(self, template, context):
        # Process {{ }} for escaped output
        template = re.sub(
            r"{{\s*(.*?)\s*}}",
            lambda match: str(self._safe_eval(match.group(1), context)),
            template
        )

        # Process {!! !!} for unescaped output
        template = re.sub(
            r"{!!\s*(.*?)\s*!!}",
            lambda match: str(self._safe_eval(match.group(1), context)),
            template
        )

        return template

class ControlStructureHandler(DirectiveHandlerBase):
    def process_control_structures(self, template, context):
        # Remove comments
        template = CommentHandler().process_comments(template)

        # Process @python blocks
        template = PythonHandler().process_python(template, context)

        # Process @isset and @empty
        template = self.process_isset_empty(template, context)

        # Process @switch statements
        template = self.process_switch_statements(template, context)

        # Process @foreach loops
        template = self.process_foreach_loops(template, context)

        # Process @for loops
        template = self.process_for_loops(template, context)

        # Process @if statements
        template = self.process_if_statements(template, context)

        # Process @break and @continue directives
        template = self.process_break_continue_in_directives(template)

        # Process variables
        template = VariableHandler().process_variables(template, context)

        return template

    def process_break_continue_in_directives(self, template):
        def break_continue_replacer(match):
            directive = match.group(0)
            if directive == '@break':
                raise BreakLoop
            elif directive == '@continue':
                raise ContinueLoop
            else:
                return ''
        return re.sub(r'@break|@continue', break_continue_replacer, template)

    def process_isset_empty(self, template, context):
        # Process @isset
        isset_pattern = r"@isset\(\s*(['\"])(.*?)\1\s*\)([\s\S]*?)@endisset"

        def isset_replacer(match):
            var_name = match.group(2).strip()
            body = match.group(3)
            if var_name in context and context[var_name] is not None:
                return self.process_control_structures(body, context)
            else:
                return ''

        template = re.sub(isset_pattern, isset_replacer, template, flags=re.DOTALL)

        # Process @empty
        empty_pattern = r"@empty\(\s*(['\"])(.*?)\1\s*\)([\s\S]*?)@endempty"

        def empty_replacer(match):
            var_name = match.group(2).strip()
            body = match.group(3)
            if not context.get(var_name):
                return self.process_control_structures(body, context)
            else:
                return ''

        return re.sub(empty_pattern, empty_replacer, template, flags=re.DOTALL)

    def process_switch_statements(self, template, context):
        pattern = r'@switch\((.*?)\)([\s\S]*?)@endswitch'

        def switch_replacer(match):
            switch_expr = match.group(1).strip()
            switch_body = match.group(2)
            switch_value = self._safe_eval(switch_expr, context)

            # Pattern to match @case and @default
            case_pattern = r'@case\((.*?)\)([\s\S]*?)(?=@case\(|@default|@endswitch)'
            default_pattern = r'@default([\s\S]*?)$'

            # Find all cases
            cases = re.findall(case_pattern, switch_body, flags=re.DOTALL)
            default = re.search(default_pattern, switch_body, flags=re.DOTALL)

            for case_expr, case_body in cases:
                case_value = self._safe_eval(case_expr.strip(), context)
                if switch_value == case_value:
                    # Remove @break directives in case body
                    case_body = re.sub(r'@break', '', case_body)
                    return self.process_control_structures(case_body, context)

            if default:
                default_body = default.group(1)
                # Remove @break directives in default body
                default_body = re.sub(r'@break', '', default_body)
                return self.process_control_structures(default_body, context)

            return ''

        return re.sub(pattern, switch_replacer, template, flags=re.DOTALL)

    def process_foreach_loops(self, template, context):
        pattern = r'@foreach\s*([\s\S]*?)@endforeach'

        def foreach_replacer(match):
            content = match.group(1)
            # Split content into loop header and loop body
            content = content.lstrip()
            lines = content.split('\n', 1)
            if len(lines) < 2:
                raise ValueError("Invalid @foreach loop syntax")
            loop_header = lines[0].strip()
            loop_body = lines[1]

            # Parse the loop header (e.g., 'item in items')
            try:
                loop_var, iterable_expr = loop_header.split(' in ', 1)
                loop_var = loop_var.strip()
                iterable_expr = iterable_expr.strip()
                iterable = self._safe_eval(iterable_expr, context)
            except Exception as e:
                raise ValueError(f"Error parsing @foreach loop header '{loop_header}': {e}")

            output = ''
            # Prepare local context
            local_context = context.copy()

            try:
                for value in iterable:
                    loop_context = local_context.copy()
                    loop_context[loop_var] = value
                    try:
                        rendered_body = self.process_control_structures(loop_body, loop_context)
                        output += rendered_body
                    except ContinueLoop:
                        continue
                    except BreakLoop:
                        break
                return output
            except Exception as e:
                raise ValueError(f"Error in @foreach loop: {e}")

        return re.sub(pattern, foreach_replacer, template, flags=re.DOTALL)

    def process_for_loops(self, template, context):
        pattern = r'@for\s*([\s\S]*?)@endfor'

        def for_replacer(match):
            content = match.group(1)
            # Split content into loop header and loop body
            content = content.lstrip()
            lines = content.split('\n', 1)
            if len(lines) < 2:
                raise ValueError("Invalid @for loop syntax")
            loop_header = lines[0].strip()
            loop_body = lines[1]

            # Parse the loop header (e.g., 'i in range(3)')
            try:
                loop_var, iterable_expr = loop_header.split(' in ', 1)
                loop_var = loop_var.strip()
                iterable_expr = iterable_expr.strip()
                iterable = self._safe_eval(iterable_expr, context)
            except Exception as e:
                raise ValueError(f"Error parsing @for loop header '{loop_header}': {e}")

            output = ''
            # Prepare local context
            local_context = context.copy()

            try:
                for value in iterable:
                    loop_context = local_context.copy()
                    loop_context[loop_var] = value
                    try:
                        rendered_body = self.process_control_structures(loop_body, loop_context)
                        output += rendered_body
                    except ContinueLoop:
                        continue
                    except BreakLoop:
                        break
                return output
            except Exception as e:
                raise ValueError(f"Error in @for loop: {e}")

        return re.sub(pattern, for_replacer, template, flags=re.DOTALL)

    def process_if_statements(self, template, context):
        pattern = r'@if\(([^)]+)\)(.*?)@endif'

        def if_replacer(match):
            condition = match.group(1).strip()
            inner_block = match.group(2).strip()

            # Split inner block into true block, elseif blocks, and else block
            blocks = re.split(r'(@elseif\([^)]+\)|@else)', inner_block)

            true_block = blocks[0].strip() if blocks else ''
            elseif_blocks = blocks[1:-1] if len(blocks) > 1 else []
            else_block = blocks[-1].strip() if blocks and blocks[-1].startswith('@else') else ''

            # Evaluate the @if condition
            if self._safe_eval(condition, context):
                return self.process_control_structures(true_block, context)

            # Process @elseif blocks
            for elseif_block in elseif_blocks:
                if elseif_block.startswith('@elseif'):
                    elseif_condition = re.match(r'@elseif\(([^)]+)\)', elseif_block).group(1).strip()
                    elseif_content = inner_block.split(elseif_block, 1)[-1].strip()
                    if self._safe_eval(elseif_condition, context):
                        return self.process_control_structures(elseif_content, context)

            # Process @else block
            if else_block:
                return self.process_control_structures(else_block.replace('@else', '').strip(), context)

            return ''

        return re.sub(pattern, if_replacer, template, flags=re.DOTALL)

class TemplateParser:
    def __init__(self, engine):
        self.engine = engine
        self.extends_handler = ExtendsHandler(engine)
        self.include_handler = IncludeHandler(engine)
        self.control_structure_handler = ControlStructureHandler()
        self.comment_handler = CommentHandler()
        self.python_handler = PythonHandler()
        self.variable_handler = VariableHandler()

    def parse(self, template, context):
        # Process @extends first
        template = self.extends_handler.process_extends(template, context, self)
        # Process the combined template (includes and directives)
        template = self.process_template(template, context)
        return template

    def process_template(self, template, context):
        # Process includes
        template = self.include_handler.process_includes(template, context, self)
        # Process directives
        template = self.process_directives(template, context)
        return template

    def process_directives(self, template, context):
        # Process control structures and variables
        template = self.control_structure_handler.process_control_structures(template, context)
        return template

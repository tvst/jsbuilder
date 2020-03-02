# Copyright 2020 Thiago Teixeira
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
jsbuild -- write JavaScript in Python
==================================

Just annotate a Python function with `@js` and then call `str()` on it to get
a fully-working JavaScript version of that function.

Example
-------

>>> from jsbuild import js
>>>
>>> @js
... def js_code():
...     bleed = 100
...     width = 960
...     height = 760
...
...     pack = (d3.layout.pack()
...         .sort(None)
...         .size([width, height + bleed * 2])
...         .padding(2))
...
...     svg = (d3.select("body").append("svg")
...         .attr("width", width)
...         .attr("height", height)
...         .append("g")
...         .attr("transform", "translate(0," + (-bleed) + ")"))
...
...     def json_read(js, error, json):
...         if error:
...             raise error
...
...         node = (svg.selectAll(".node")
...             .data(pack.nodes(flatten(json)))
...             .filter(lambda d: not d.children)
...             .enter()
...                 .append("g")
...                 .attr("class", "node")
...                 .attr("transform", lambda d: "translate(" + d.x + "," + d.y + ")"))
...
...         (node.append("circle")
...             .attr("r", lambda d: d.r))
...
...         (node.append("text")
...             .text(lambda d: d.name)
...             .style("font-size", lambda d: Math.min(2 * d.r, (2 * d.r - 8) / getComputedTextLength() * 24) + "px")
...             .attr("dy", ".35em"))
...
...     d3.json("README.json", json_read)
...
>>>
>>> str(js_code)
'bleed = 100;\nwidth = 960;\nheight = 760;\npack = d3.layout.pack().sort(null).size([width, (height + (bleed * 2))]).padding(2);\nsvg = d3.select("body").append("svg").attr("width", width).attr("height", height).append("g").attr("transform", (("translate(0," + (-bleed)) + ")"));\nfunction json_read(js, error, json) {\nif (error) {\nthrow new Error(\'error\')\n} else {\n\n};\nnode = svg.selectAll(".node").data(pack.nodes(flatten(json))).filter(((d) => ((!d.children)))).enter().append("g").attr("class", "node").attr("transform", ((d) => ((((("translate(" + d.x) + ",") + d.y) + ")"))));\nnode.append("circle").attr("r", ((d) => (d.r)));\nnode.append("text").text(((d) => (d.name))).style("font-size", ((d) => ((Math.min((2 * d.r), ((((2 * d.r) - 8) / getComputedTextLength()) * 24)) + "px")))).attr("dy", ".35em")\n};\nd3.json("README.json", json_read)'
>>>
>>> print(js_code)
bleed = "100";
width = "960";
height = "760";
pack = "d3.layout.pack().sort(null).size([width, (height + (bleed * 2))])".padding("2");
svg = "d3.select("body").append("svg").attr("width", width).attr("height", height).append("g")".attr(""transform"", ("("translate(0," + (-bleed))" "+" "")""));
function json_read("js, error, json") {
"if (error) {
throw new Error('error')
} else {
};
node = svg.selectAll(".node").data(pack.nodes(flatten(json))).filter(((d) => ((!d.children)))).enter().append("g").attr("class", "node").attr("transform", ((d) => ((((("translate(" + d.x) + ",") + d.y) + ")"))));
node.append("circle").attr("r", ((d) => (d.r)));
node.append("text").text(((d) => (d.name))).style("font-size", ((d) => ((Math.min((2 * d.r), ((((2 * d.r) - 8) / getComputedTextLength()) * 24)) + "px")))).attr("dy", ".35em")"
};
"d3.json("README.json", json_read)"

"""

import inspect
import ast


def js(func):
    return JSFunc(func)


class JSFunc(object):
    def __init__(self, func):
        self._ast = ast.parse(inspect.getsource(func))
        self._orig = func

    def __str__(self):
        return _to_str(self._ast.body[0].body)

    def __call__(self, *args, **kwargs):
        return self._orig(*args, **kwargs)


def _parse_assign(node):
    targets = " = ".join(_to_str_iter(node.targets))
    return "%s = %s" % (targets, _to_str(node.value))


def _parse_bool_op(node):
    op = _to_str(node.op)
    return op.join(_to_str_iter(node.values))


def _parse_compare(node):
    ops = _to_str_iter(node.ops)
    comparators = _to_str_iter(node.comparators)
    ops_comps = zip(ops, comparators)
    return "%s %s" % (
        _to_str(node.left),
        " ".join("%s %s" % oc for oc in ops_comps),
    )


def _parse_call(node):
    func = _to_str(node.func)
    args = _to_str_iter(node.args)
    return "%s(%s)" % (
        func,
        ", ".join(args),
    )


# See:
# - https://docs.python.org/3/library/ast.html
# - https://greentreesnakes.readthedocs.io/en/latest/nodes.html
_PARSERS = {
    #"Module":
    "FunctionDef": "function %(raw_name)s(%(args)s) {\n%(body)s\n}",
    #"AsyncFunctionDef":
    #"ClassDef": _parse_class_def,  # Need to figure out "new" JS keyword.
    "Return": "return %(value)s",
    "Delete": "delete %(targets)s",
    "Assign": _parse_assign,
    #"AugAssign": _parse_aug_assign,
    #"AnnAssign":
    #"For": _parse_for,
    #"AsyncFor":
    "While": "while (%(test)s) {\n%(body)s\n}",
    "If": "if (%(test)s) {\n%(body)s\n} else {\n%(orelse)s\n}",
    #"With":
    #"AsyncWith":
    "Raise": "throw new Error('%(exc)s')",
    #"Try": _parse_try,
    #"TryFinally": _parse_try_finally,
    #"TryExcept": _parse_try_except,
    #"Assert":
    #"Import":
    #"ImportFrom":
    #"Global":
    #"Nonlocal":
    "Expr": "%(value)s",
    "Pass": "",
    "BoolOp": _parse_bool_op,
    #"NamedExpr": _parse_named_expr,
    "BinOp": "(%(left)s %(op)s %(right)s)",
    "UnaryOp": "(%(op)s%(operand)s)",
    "Lambda": "((%(args)s) => (%(body)s))",
    "IfExp": "(%(test)s) ? (%(body)s) : (%(orelse)s)",
    #"Dict":
    #"Set":
    #"ListComp":
    #"SetComp":
    #"DictComp":
    #"GeneratorExp":
    #"Await":
    #"Yield":
    #"YieldFrom":
    "Compare": _parse_compare,
    "Call": _parse_call,
    #"FormattedValue":
    #"JoinedStr":
    "Constant": "%(value)s",
    "Attribute": "%(value)s.%(raw_attr)s",
    "Subscript": "%(value)s[%(slice)s]",
    #"Starred":
    "Name": "%(raw_id)s",
    "List": lambda l: "[%s]" % ', '.join(_to_str(x) for x in l.elts),
    #"Tuple": _parse_tuple,
    #"AugLoad":
    #"AugStore":
    #"Param": _parse_param,
    #"Slice":
    #"ExtSlice":
    "Index": "%(value)s",
    "And": "&&",
    "Or": "||",
    "Add": "+",
    "Sub": "-",
    "Mult": "*",
    #"MatMult":
    "Div": "/",
    "Mod": "%",
    #"Pow":
    "LShift": "<<",
    "RShift": ">>",
    "BitOr": "|",
    "BitXor": "^",
    "BitAnd": "&",
    #"FloorDiv": ,
    "Invert": "~",
    "Not": "!",
    "UAdd": "+",
    "USub": "-",
    "Eq": "===",
    "NotEq": "!==",
    "Lt": "<",
    "LtE": "<=",
    "Gt": ">",
    "GtE": ">=",
    #"Is":
    #"IsNot":
    #"In":
    #"NotIn":
    #"ExceptHandler": _parse_except_handler,
    "Break": "break",
    "Continue": "continue",
    "arguments": lambda arguments: ', '.join(x.arg for x in arguments.args),

    # For Python < 3.8
    "Num": "%(n)s",
    "Str": '"%(s)s"',
    "Bytes": '"%(s)s"',
    #"Ellipsis
    "NameConstant": "%(value)s",
}


def _to_str(node):
    node_type = type(node)

    if node_type is list:
        return ';\n'.join(_to_str(x) for x in node)

    if node is None:
        return "null"

    if node_type is str:
        return '"%s"' % node

    if node_type in (int, float):
        return str(node)

    if node_type.__name__ not in _PARSERS:
        raise Exception("Unsupported operation in JS: %s" % node_type)

    parser = _PARSERS[node_type.__name__]

    if type(parser) is str:
        return parser % _DictWrapper(node.__dict__)

    return parser(node)


class _DictWrapper(dict):
    def __init__(self, dikt):
        self._dict = dikt
        self._parsed_keys = set()

    def __getitem__(self, k):
        raw = False

        if k.startswith("raw_"):
            k = k[4:]
            raw = True

        if k not in self._parsed_keys:
            if raw:
                self._dict[k] = self._dict[k]
            else:
                self._dict[k] = _to_str(self._dict[k])
            self._parsed_keys.add(k)

        return self._dict[k]


def _to_str_iter(arg):
    return (_to_str(x) for x in arg)

# jsbuild — convert Python code to JavaScript strings

Just annotate a Python function with `@js` and then call `str()` on it to get
a fully-working JavaScript version of that function. Why? _Because why not._

(If you like this, check out [htbuild](https://github.com/tvst/htbuild). It's the
HTML equivalent of jsbuild: an HTML string builder for Python folks who don't
like templating languages.)

## Simple Example

```py
from jsbuild import js

@js
def js_code():

  def sum_and_check_if_42(a, b):
    c = a + b
    if c == 42:
      return True
    else:
      return False

  result = sum_and_check_if_42(10, 30)
  console.log("Is it 42?", result)
```

Now you can just call `str(js_code)` or `print(js_code)` to see the JavaScript
version of that code:

_(Note: the code below has been pretty-printed for clarity)_

```js
function sum_and_check_if_42(a, b) {
  c = (a + b);

  if (c === 42) {
    return true
  } else {
    return false
  }
};

result = sum_and_check_if_42(10, 30);
console.log("Is it 42?", result)
```

## Complex Example

Here's some code that was copy/pasted directly from the D3 documentation,
then converted to Python:

```py
from jsbuild import js

@js
def js_code():
    bleed = 100
    width = 960
    height = 760

    pack = (d3.layout.pack()
            .sort(None)
            .size([width, height + bleed * 2])
            .padding(2))

    svg = (d3.select("body").append("svg")
           .attr("width", width)
           .attr("height", height)
           .append("g")
           .attr("transform", "translate(0," + (-bleed) + ")"))

    def json_read(js, error, json):
        if error:
            raise error

        node = (svg.selectAll(".node")
                .data(pack.nodes(flatten(json)))
                .filter(lambda d: not d.children)
                .enter()
                .append("g")
                .attr("class", "node")
                .attr("transform", lambda d: "translate(" + d.x + "," + d.y + ")"))

        (node.append("circle")
         .attr("r", lambda d: d.r))

        (node.append("text")
         .text(lambda d: d.name)
         .style("font-size", lambda d: Math.min(2 * d.r, (2 * d.r - 8) / getComputedTextLength() * 24) + "px")
         .attr("dy", ".35em"))

    d3.json("README.json", json_read)

    def flatten(root):
        nodes = []

        def recurse(node):
            if node.children:
                node.children.forEach(recurse)
            else:
                nodes.push({"name": node.name, "value": node.size})

        recurse(root)
        return {"children": nodes}
```

And the JS-converted version is:

```js
bleed = 100;
width = 960;
height = 760;

pack = d3.layout
    .pack()
    .sort(null)
    .size([width, (height + (bleed * 2))])
    .padding(2);

svg = d3.select("body")
    .append("svg")
    .attr("width", width).attr("height", height)
    .append("g")
    .attr("transform", (("translate(0," + (-bleed)) + ")"));

function json_read(js, error, json) {
    if (error) {
        throw new Error(error)
    } else {
    };
    node = svg.selectAll(".node")
        .data(pack.nodes(flatten(json)))
        .filter(((d) => ((!d.children))))
        .enter()
            .append("g")
            .attr("class", "node")
            .attr("transform", ((d) => (
                (((("translate(" + d.x) + ",") + d.y) + ")"))));
    node.append("circle")
        .attr("r", ((d) => (d.r)));
    node.append("text")
        .text(((d) => (d.name)))
        .style("font-size", ((d) => (
            (Math.min(
                (2 * d.r),
                ((((2 * d.r) - 8) / getComputedTextLength()) * 24)
            ) + "px"))))
        .attr("dy", ".35em")
};

d3.json("README.json", json_read);

function flatten(root) {
    nodes = [];

    function recurse(node) {
        if (node.children) {
            node.children.forEach(recurse)
        } else {
            nodes.push({"name": node.name, "value": node.size})
        }
    };

    recurse(root);
    return {"children": nodes}
}
```

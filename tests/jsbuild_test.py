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

import re

import unittest

from jsbuild import js


class TestHtBuild(unittest.TestCase):
    def test_empty(self):
        @js
        def js_code():
            pass

        actual = str(js_code)
        expected = ''
        self.assertEqual(actual, expected)

    def test_simple_assignment(self):
        @js
        def js_code():
            a = 10

        actual = str(js_code)
        expected = 'a = 10'
        self.assertEqual(actual, expected)

    def test_simple_example(self):
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

        actual = str(js_code)
        expected = '''
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
        '''

        self.assertEqual(
            remove_whitespace(actual),
            remove_whitespace(expected)
        )

    def test_complex_example(self):
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

        actual = str(js_code)
        expected = '''
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
        '''

        self.assertEqual(
            remove_whitespace(actual),
            remove_whitespace(expected)
        )



WHITESPACE = re.compile(r'\s+')

def remove_whitespace(s):
    return WHITESPACE.sub('', s)


if __name__ == '__main__':
    unittest.main()

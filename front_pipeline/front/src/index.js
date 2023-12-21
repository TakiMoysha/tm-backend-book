import _ from "lodash";

const root_id = "spa-vue-app";

const element = {
  type: "h1",
  props: {
    title: "foo",
    children: "Hello world!",
  },
};
const container = document.getElementById(root_id);

const node = document.createElement(element.type);
node["title"] = element.props.title;
const text = document.createTextNode("");
text["nodeValue"] = element.props.children;

node.appendChild(text);
container.appendChild(node);
console.log("Done")

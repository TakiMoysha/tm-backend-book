import _ from "lodash";

const root_id = "native-root";

const createTextElement = (text) => {
  return {
    type: "TEXT_ELEMENT",
    props: {
      nodeValue: text,
      children: [],
    },
  };
};

const createElement = (type, props, ...children) => {
  return {
    type,
    props: {
      ...props,
      children: children.map((child) =>
        typeof child === "object" ? child : createTextElement(child),
      ),
    },
  };
};

const render = (el, container) => {
  const dom =
    element.type == "TEXT_ELEMENT"
      ? document.createTextNode("")
      : document.createElement(element.type);

  // const isProperty = (key) => key !== "children";
  // Object.key(el.props)
  //   .filter(isProperty)
  //   .foreach((name) => {
  //     dom[name] = element.props[name];
  //   });
  // el.props.children.forEach((element) => {
  //   render(child, dom);
  // });

  let nextNodeProcess = null;

  const nodeProcessLoop = (deadline) => {
    let shouldProcess = false
    while (nextNodeProcess && !shouldProcess) {
      nextNodeProcess = performNodeProcess(nextNodeProcess)
      shouldProcess = deadline.timeRemaining() < 1
    }
    requestIdleCb(nodeProcessLoop)
  }
  requestIdleCallback(nodeProcessLoop)

  container.appendChild(dom);
};

const Didact = {
  createElement,
  render,
};

// const node = document.createElement(el.type);
// node["title"] = el.props.title;
// const text = document.createTextNode("");
// text["nodeValue"] = el.props.children;
//
// node.appendChild(text);
// container.appendChild(node);
// console.log("Done")

console.log("rendering");
const newEl = Didact.createElement("div", { id: root_id });
console.log(newEl)
// Didact.render(newEl);
console.log("end");

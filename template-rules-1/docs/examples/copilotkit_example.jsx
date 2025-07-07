import React from "react";
import { CopilotKit, useCopilotAction } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";

const MyCopilotKitComponent = () => {
  useCopilotAction({
    name: "sayHello",
    description: "Says hello to someone.",
    parameters: [
      {
        name: "name",
        type: "string",
        description: "The name of the person to say hello to.",
      },
    ],
    handler: ({ name }) => {
      alert(`Hello, ${name}!`);
    },
  });

  return (
    <CopilotKit url="/api/copilotkit">
      <CopilotPopup />
    </CopilotKit>
  );
};

export default MyCopilotKitComponent;

// To use this example:
// 1. Install the necessary packages: npm install @copilotkit/react-core @copilotkit/react-ui
// 2. Set up the CopilotKit backend service at /api/copilotkit
// 3. Integrate this component into your React application.

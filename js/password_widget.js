import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "your.node.password",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "YourNodeName") { // Replace with your actual node name
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // Find the token widget and make it a password field
                const tokenWidget = this.widgets.find(w => w.name === "token");
                if (tokenWidget && tokenWidget.inputEl) {
                    tokenWidget.inputEl.type = "password";
                }
                
                return r;
            };
        }
    }
});
import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "your.downloader.password",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Handle CivitAI Downloader
        if (nodeData.name === "CivitAIDownloader") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                setTimeout(() => {
                    const tokenWidget = this.widgets?.find(w => w.name === "token_id");
                    if (tokenWidget?.inputEl) {
                        tokenWidget.inputEl.type = "password";
                    }
                }, 100);
                
                return r;
            };
        }
        
        // Handle HF Downloader
        if (nodeData.name === "HFDownloader") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                setTimeout(() => {
                    const hfTokenWidget = this.widgets?.find(w => w.name === "hf_token");
                    if (hfTokenWidget?.inputEl) {
                        hfTokenWidget.inputEl.type = "password";
                    }
                }, 100);
                
                return r;
            };
        }
    }
});
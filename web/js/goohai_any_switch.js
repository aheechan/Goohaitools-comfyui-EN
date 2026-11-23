import { app } from "../../../scripts/app.js";

const MAX_INPUTS = 16;
const MIN_INPUTS = 2;
// LiteGraph uses a 20px slot row. Keep the title and bottom spacing explicit so
// the bottom blank area stays fixed at 10px as inputs are added or removed.
const INPUT_ROW_HEIGHT = 20;
const NODE_HEADER_HEIGHT = 30;
const BOTTOM_PADDING = 10;
const INITIAL_HEIGHT = NODE_HEADER_HEIGHT + MIN_INPUTS * INPUT_ROW_HEIGHT + BOTTOM_PADDING;
const INITIAL_SIZE = [300, INITIAL_HEIGHT];
const slotName = (index) => `any_${String(index + 1).padStart(2, "0")}`;
const slotNumber = (index) => String(index + 1).padStart(2, "0");
const heightForInputCount = (count) =>
    NODE_HEADER_HEIGHT + Math.max(0, Number(count) || 0) * INPUT_ROW_HEIGHT + BOTTOM_PADDING;
const validSize = (size) => {
    const width = Array.isArray(size) || ArrayBuffer.isView(size)
        ? size[0]
        : size?.width;
    const height = Array.isArray(size) || ArrayBuffer.isView(size)
        ? size[1]
        : size?.height;
    return Number.isFinite(Number(width))
        && Number.isFinite(Number(height))
        && Number(width) > 0
        && Number(height) > 0
        ? [Number(width), Number(height)]
        : null;
};

app.registerExtension({
    name: "goohaitools.any_switch",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "GoohaiAnySwitch") return;

        const labels = {
            IMAGE: "Image",
            VIDEO: "Video",
            AUDIO: "Audio",
            MASK: "Mask",
            LATENT: "latent",
            MODEL: "Model",
            CLIP: "CLIP",
            CLIP_VISION: "CLIP Vision",
            CLIP_VISION_OUTPUT: "CLIP Vision Output",
            VAE: "VAE",
            CONDITIONING: "Conditioning",
            CONDITION: "Conditioning",
            CONTROL_NET: "ControlNet",
            STYLE_MODEL: "Style Model",
            GLIGEN: "GLIGEN",
            UPSCALE_MODEL: "Upscale Model",
            GUIDER: "Guider",
            SAMPLER: "Sampler",
            SIGMAS: "Sigmas",
            SIGMA: "Sigma",
            NOISE: "Noise",
            TENSOR: "Tensor",
            COMBO: "Combo",
            IMAGE_BATCH: "Image Batch",
            MASK_BATCH: "Mask Batch",
            LATENT_BATCH: "Latent Batch",
            LIST: "List",
            STRING: "String",
            INT: "Integer",
            FLOAT: "Float",
            BOOLEAN: "Boolean",
            BBOX: "BBox",
            SEGS: "Segments",
            FACE_ANALYSIS: "Face Analysis",
            ANY: "any",
        };

        const connected = (slot) => slot?.link != null;

        const getConnectedType = function () {
            const types = new Set();
            for (const slot of this.inputs || []) {
                if (!connected(slot)) continue;
                const link = this.graph?.links?.[slot.link];
                const origin = link && this.graph?.getNodeById?.(link.origin_id);
                const output = origin?.outputs?.[link.origin_slot];
                const type = output?.type && String(output.type).toUpperCase();
                if (type && type !== "*" && type !== "ANY") types.add(type);
            }
            // A mixed graph is left as ANY in the UI. The backend performs the
            // definitive type check and reports the conflicting input types.
            return types.size === 1 ? [...types][0] : "ANY";
        };

        const sync = function () {
            let slots = this.inputs || [];

            // A copied/restored node can contain stale trailing inputs. Hard cap
            // the visible slots so repeated lifecycle events can never grow it.
            while (slots.length > MAX_INPUTS) {
                this.removeInput(slots.length - 1);
                slots = this.inputs || [];
            }

            let lastConnected = -1;
            slots.forEach((slot, index) => {
                if (connected(slot)) lastConnected = index;
            });

            const target = Math.min(
                MAX_INPUTS,
                Math.max(MIN_INPUTS, lastConnected + 2),
            );

            // Only trailing empty slots are removed. A gap in the middle keeps
            // its original position so backend priority remains stable.
            while ((this.inputs || []).length > target) {
                const index = this.inputs.length - 1;
                if (connected(this.inputs[index])) break;
                this.removeInput(index);
            }
            while ((this.inputs || []).length < target) {
                const index = this.inputs.length;
                this.addInput(slotName(index), "*");
            }

            slots = this.inputs || [];
            const type = getConnectedType.call(this);
            const slotType = type === "ANY" ? "*" : type;

            slots.forEach((slot, index) => {
                // `name` is the serialized/backend key and must never change.
                // Type-specific text belongs only in the visible label.
                slot.name = slotName(index);
                slot.label = type === "ANY"
                    ? slot.name
                    : `${labels[type] || type}_${slotNumber(index)}`;
                slot.type = slotType;
            });

            const output = this.outputs?.[0];
            if (output) {
                output.name = "any";
                output.label = type === "ANY" ? "any" : (labels[type] || type);
                output.type = slotType;
            }

            // Keep the manually selected width, while deriving the height from
            // the current input count. The compact base height includes the
            // fixed title and bottom spacing; each additional input adds one row.
            const currentWidth = Number(this._ghAnySwitchRestoreWidth)
                || Number(this.size?.[0])
                || INITIAL_SIZE[0];
            this.setSize?.([currentWidth, heightForInputCount(slots.length)]);
            this._ghAnySwitchRestoreWidth = null;

            this.setDirtyCanvas?.(true, true);
        };

        const scheduleSync = function () {
            if (this._ghAnySwitchSyncScheduled) return;
            this._ghAnySwitchSyncScheduled = true;
            requestAnimationFrame(() => {
                this._ghAnySwitchSyncScheduled = false;
                sync.call(this);
            });
        };

        const originalCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            originalCreated?.apply(this, arguments);
            // Keep newly created nodes compact. onConfigure can subsequently
            // restore a deliberately saved width from an existing workflow.
            if (!this._ghAnySwitchInitialized) {
                this.setSize?.(INITIAL_SIZE);
                this._ghAnySwitchInitialized = true;
            }
            // Do not remove inputs synchronously here: onConfigure may still be
            // restoring serialized links. The idempotent sync below handles both
            // a fresh node and a restored/copied node after that lifecycle step.
            scheduleSync.call(this);
        };

        const originalConnections = nodeType.prototype.onConnectionsChange;
        nodeType.prototype.onConnectionsChange = function () {
            originalConnections?.apply(this, arguments);
            scheduleSync.call(this);
        };

        const originalConfigure = nodeType.prototype.onConfigure;
        nodeType.prototype.onConfigure = function (config) {
            originalConfigure?.apply(this, arguments);
            const savedSize = validSize(config?.size);
            if (savedSize) this._ghAnySwitchRestoreWidth = savedSize[0];
            scheduleSync.call(this);
        };
    },
});

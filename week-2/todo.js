"use strict";
var ItemState;
(function (ItemState) {
    ItemState["DONE"] = "Done";
    ItemState["NOT_DONE"] = "Not Done";
    ItemState["IN_PROGRESS"] = "In Progress";
    ItemState["UNDER_REVIEW"] = "Under Review";
    ItemState["BLOCKED"] = "Blocked";
})(ItemState || (ItemState = {}));
var ItemPriority;
(function (ItemPriority) {
    ItemPriority[ItemPriority["HIGH"] = 1] = "HIGH";
    ItemPriority[ItemPriority["MEDIUM"] = 2] = "MEDIUM";
    ItemPriority[ItemPriority["LOW"] = 3] = "LOW";
})(ItemPriority || (ItemPriority = {}));

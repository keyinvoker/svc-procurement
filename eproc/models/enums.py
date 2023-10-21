from enum import Enum


class SystemConfigOption(Enum):
    APPROVAL_LIMIT_PR_PROJECT = "PR Project Approval Limit"
    APPROVAL_LIMIT_PRICE_COMPARISON = "Comparison Approval Limit"
    APPROVAL_LIMIT_PURCHASE_ORDER = "PO Approval Limit"
    APPROVAL_LIMIT_GOODS_RECEIVED = "Goods Received Limit"
    PURCHASE_ORDER = "Required Date PO"
    SYSTEM_LOCK = "Time"
    PASSWORD = "Password"
    ACCESS_TIME = "Access Time"
    UPLOAD = "Upload"
    TAX = "PPH"

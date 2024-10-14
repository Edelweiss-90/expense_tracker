from enum import Enum


class DeletedStatuses(Enum):
    NOT_DELETED = 'NOT_DELETED'
    CASCADE_DELETED = 'CASCADE_DELETED'
    PERMANENTLY_DELETED = 'PERMANENTLY_DELETED'


class TableName(Enum):
    USER = 'user'
    CATEGORY = 'category'
    TRANSACTION = 'transaction'

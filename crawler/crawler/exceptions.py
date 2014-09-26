from scrapy.exceptions import DropItem


class PaidLinkException(DropItem):
    pass


class IncorrectFormatException(DropItem):
    pass


class IncorrectPriceException(DropItem):
    pass


class InvalidPriceException(DropItem):
    pass


class UnknownSpiderException(DropItem):
    pass


class OldItemException(DropItem):
    pass


class NotinterestingItemException(DropItem):
    pass


class AlreadyCrawledException(DropItem):
    pass

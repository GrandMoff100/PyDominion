class DominionError(Exception):
    pass


class BuyError(DominionError):
    pass


class EmptySupplyPileError(BuyError):
    pass


class NoBuysAvailableError(BuyError):
    pass


class UnaffordableError(BuyError):
    pass


class ActionError(DominionError):
    pass


class IllegalEffectError(ActionError):
    pass


class NoActionsAvailableError(ActionError):
    pass


class CardNotFoundError(ActionError):
    pass


class PlayerNotFoundError(DominionError):
    pass

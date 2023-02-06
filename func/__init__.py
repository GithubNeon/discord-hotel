from .color import *
from .emojis import *
from .musicSearch import *
from .locale import *


def isKo(interaction: nextcord.Interaction):
    return interaction.locale == "ko"

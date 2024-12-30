import discord
from discord.ext.localization import Localization
from dataclasses import dataclass, field
from typing import Optional
import datetime

class A:
    def __init__(self):
        self.a = 1

a = A()

localization_data = {
    "en": {
        "nested": {
            "first": "first nested thing",
            "second": {
                "fourth": "fourth nested thing with a kwarg {user}",
                "fifth": "fifth nested thing with a kwarg {user.name}"
            }
        }
    }
}

@dataclass
class CustomUser:
    _name: str = field(repr=False)
    id: int
    """Returns the user's ID."""
    _discriminator: str = field(repr=False)
    global_name: str = field(repr=False)
    """Returns the user's global display name. The hierarchy is as follows:
    
    1. ``name#discriminator`` if the user has a discriminator (only bots).
    2. ``global_name`` if the user has a global name.
    3. ``name`` if the user has neither a discriminator nor a global name."""
    display_name: str = field(repr=False)
    """Returns the user's display name. This is the name that is shown in the server if they are a member.
    Otherwise, it is the same as ``global_name``."""
    bot: bool
    """Returns whether or not the user is a Discord bot."""
    _color: Optional[discord.Colour] = field(repr=False)
    _avatar: str = field(repr=False)
    _decoration: Optional[str] = field(repr=False)
    _banner: Optional[str] = field(repr=False)
    _created_at: datetime.datetime = field(repr=False)
    mention: str
    """Returns a string that mentions the user."""

    @classmethod
    def from_user(cls, user: discord.User):
        """Creates a ``CustomUser`` from a ``discord.User`` object."""
        return cls(
            _name=f"{user.name}#{user.discriminator}",
            id=user.id,
            _discriminator=user.discriminator,
            global_name=f"{user.name}#{user.discriminator}",
            display_name=user.display_name or \
                         (f"{user.name}#{user.discriminator}"),
            bot=user.bot,
            _color=user.accent_color,
            _avatar=user.display_avatar.url,
            _decoration=user.avatar_decoration.url,
            _banner=user.banner.url if user.banner else "",
            _created_at=user.created_at,
            mention=user.mention
        )

    @property
    def name(self) -> str:
        """Returns the username of the user."""
        return self._name

    user_name = user = username = name

    @property
    def discriminator(self) -> str:
        """Returns the discriminator of the user. This is a legacy concept that only applies to bots."""
        return self._discriminator

    tag = discriminator

    @property
    def color(self) -> discord.Color:
        """Returns the user's accent color."""
        return self._color

    colour = color

    @property
    def avatar(self) -> str:
        """Returns the user's avatar URL."""
        return self._avatar

    icon = avatar

    @property
    def created_at(self):
        """Returns the date the user was created as a Discord timestamp. You can call this with or without brackets.
        If you call it with braces you can pass a ``DatetimeFormat`` to format the timestamp."""
        return FormatDateTime(self._created_at, "F")

    created = created_at

    def __str__(self):
        return self.global_name

    def __int__(self):
        return self.id

client = discord.Client(intents=discord.Intents.all())

class Name:
    def __init__(self, name):
        self.name = name
        self.capitalized = name.capitalize()
    
    def __str__(self):
        return self.name

_ = Localization(localization_data)
print(_("nested.second.fourth", "en", name=Name("bob")))
print(_("nested.second.fifth", "en", name=Name("bob")))
@client.event
async def on_ready():

    custom_user = CustomUser.from_user(await client.fetch_user(648168353453572117))

    # Test with placeholders=True
    text_with_placeholders = _("nested.second.fourth", "en", placeholders=True)
    print(text_with_placeholders)

    text_with_placeholders = _("nested.second.fourth", "en", placeholders=True, user=custom_user)
    print(text_with_placeholders)

    # Test with placeholders=False
    text_without_placeholders = _("nested.second.fourth", "en", placeholders=False, user=custom_user)
    print(text_without_placeholders)

    text_without_placeholders = _("nested.second.fourth", "en", placeholders=False)
    print(text_without_placeholders)

client.run("token")
from discord.ext.localization import Localization

_ = Localization("test_lang.json")
print(_("apples.one", "en"))
_.localizations = "other_test.json"
print(_("other", "en"))
new_dict = {
    "en": {
        "test": "This is a test."
    },
    "hu": {
        "test": "Ez egy teszt."
    }
}
_.file = new_dict
print(_("test", "en"))
_.localizations = "test_yaml.yml"
print(_("nested", "en", test="EXAMPLE"))
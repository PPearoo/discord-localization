from .localization import Localization as Localization

if __name__ == "__main__":
    _ = Localization("tests/test_lang.json")
    
    print(_.file)
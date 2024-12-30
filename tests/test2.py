import string

class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        # Handle missing keys by returning a placeholder
        if isinstance(key, str):
            return kwargs.get(key, f"{{{key}}}")
        return super().get_value(key, args, kwargs)

    def get_field(self, field_name, args, kwargs):
        try:
            # Try to resolve the field normally
            return super().get_field(field_name, args, kwargs)
        except (KeyError, AttributeError):
            # Return the placeholder if the key or attribute is missing
            return f"{{{field_name}}}", field_name

# Example usage
class Name:
    def __init__(self, name):
        self.name = name
        self.capitalized = name.capitalize()

    def __str__(self):
        return self.name

formatter = SafeFormatter()

# Examples
print(formatter.format("hello, {name}!", name=Name("bob")))  # hello, bob!
print(formatter.format("greetings, {name.capitalized}!", name=Name("bob")))  # greetings, Bob!
print(formatter.format("hello, {name}!", age=34))  # hello, {name}!
print(formatter.format("greetings, {name.capitalized}!", age=34))  # greetings, {name.capitalized}!

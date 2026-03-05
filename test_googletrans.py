from googletrans import Translator

translator = Translator()
result = translator.translate('Hello world', dest='ja')
print(f"Type: {type(result)}")
print(f"Result: {result}")
if hasattr(result, 'text'):
    print(f"Text attribute: {result.text}")
print(f"Attributes: {[x for x in dir(result) if not x.startswith('_')]}")

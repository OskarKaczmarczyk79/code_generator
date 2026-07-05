import json
from jinja2 import Template

# Mapowanie typów z JSON na formaty dla biblioteki struct w Pythonie
# i = integer (całkowita), f = float (zmiennoprzecinkowa), ? = boolean (prawda/fałsz)
type_mapping = {
    "int": "i",
    "float": "f",
    "bool": "?"
}

def generate_code():
    # 1. Wczytanie pliku JSON
    with open('interface.json', 'r') as f:
        data_def = json.load(f)

    # Pobranie nazwy klasy i jej pól z JSON
    class_name = list(data_def.keys())[0]
    fields_dict = data_def[class_name]
    fields_list = list(fields_dict.keys())

    # Generowanie łańcucha formatującego dla struct (np. dla int, float, bool będzie to 'if?')
    struct_format = ""
    for field_type in fields_dict.values():
        struct_format += type_mapping[field_type]

    # 2. Wczytanie szablonu Jinja2
    with open('template.j2', 'r') as f:
        template_content = f.read()

    template = Template(template_content)

    # 3. Wygenerowanie ostatecznego kodu na podstawie szablonu
    generated_code = template.render(
        class_name=class_name,
        fields=fields_list,
        struct_format=struct_format
    )

    # 4. Zapisanie wygenerowanego kodu do nowego pliku Python
    with open('protocol.py', 'w') as f:
        f.write(generated_code)

    print(f"Sukces! Wygenerowano plik protocol.py dla struktury {class_name}.")

if __name__ == "__main__":
    generate_code()
import json
from jinja2 import Template

# Mapowanie typów z JSON na formaty dla biblioteki struct w Pythonie
# i = integer (całkowita), f = float (zmiennoprzecinkowa), ? = boolean (prawda/fałsz)
type_mapping = {
    "int": "i",
    "float": "f",
    "bool": "?"
}


def generate_code_from_definition(data_def):
    class_name = list(data_def.keys())[0]
    fields_dict = data_def[class_name]
    fields = [
        {"name": field_name, "type": field_type}
        for field_name, field_type in fields_dict.items()
    ]

    # Generowanie łańcucha formatującego dla struct dla pól prostych
    struct_format = ""
    for field in fields:
        if field["type"] == "list":
            continue
        struct_format += type_mapping[field["type"]]

    with open('template.j2', 'r', encoding='utf-8') as f:
        template_content = f.read()

    template = Template(template_content)
    return template.render(
        class_name=class_name,
        fields=fields,
        struct_format=struct_format,
        type_mapping=type_mapping,
    )


def generate_code():
    # 1. Wczytanie pliku JSON
    with open('interface.json', 'r', encoding='utf-8') as f:
        data_def = json.load(f)

    generated_code = generate_code_from_definition(data_def)

    # 2. Zapisanie wygenerowanego kodu do nowego pliku Python
    with open('protocol.py', 'w', encoding='utf-8') as f:
        f.write(generated_code)

    print(f"Sukces! Wygenerowano plik protocol.py dla struktury {list(data_def.keys())[0]}.")


if __name__ == "__main__":
    generate_code()

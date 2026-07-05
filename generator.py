import argparse
import json
from pathlib import Path

from jinja2 import Template

# Mapowanie typów z JSON na formaty dla biblioteki struct w Pythonie
# i = integer (całkowita), f = float (zmiennoprzecinkowa), ? = boolean (prawda/fałsz)
type_mapping = {
    "int": "i",
    "float": "f",
    "bool": "?",
    "str": "str",
}
SUPPORTED_TYPES = set(type_mapping.keys()) | {"list"}
BASE_DIR = Path(__file__).resolve().parent


def resolve_path(path_value, default_name=None, base_dir=BASE_DIR):
    if path_value is None:
        path_value = default_name or "interface.json"

    path = Path(path_value)
    if not path.is_absolute():
        path = base_dir / path
    return path.resolve()


def validate_definition(data_def):
    if not isinstance(data_def, dict) or len(data_def) != 1:
        raise ValueError("Plik JSON musi zawierać dokładnie jedną strukturę na górze.")

    class_name, fields_dict = next(iter(data_def.items()))
    if not isinstance(class_name, str) or not isinstance(fields_dict, dict):
        raise ValueError("Nieprawidłowa struktura pliku JSON.")

    for field_name, field_type in fields_dict.items():
        if not isinstance(field_name, str):
            raise ValueError("Nazwy pól muszą być napisami.")
        if not isinstance(field_type, str):
            raise ValueError(f"Typ pola {field_name} musi być napisem.")
        if field_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Nieobsługiwany typ '{field_type}' dla pola '{field_name}'. "
                f"Obsługiwane typy: {sorted(SUPPORTED_TYPES)}"
            )

    return class_name, fields_dict


def generate_code_from_definition(data_def, template_path=None):
    class_name, fields_dict = validate_definition(data_def)
    fields = [
        {"name": field_name, "type": field_type}
        for field_name, field_type in fields_dict.items()
    ]

    struct_format = ""
    for field in fields:
        if field["type"] == "list":
            continue
        if field["type"] == "str":
            continue
        struct_format += type_mapping[field["type"]]

    template_path = template_path or BASE_DIR / "template.j2"
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    template = Template(template_content)
    return template.render(
        class_name=class_name,
        fields=fields,
        struct_format=struct_format,
        type_mapping=type_mapping,
    )


def generate_code(input_path=None, output_path=None, template_path=None):
    input_path = resolve_path(input_path, "interface.json")
    output_path = resolve_path(output_path, "protocol.py")
    template_path = resolve_path(template_path, "template.j2") if template_path else BASE_DIR / "template.j2"

    with open(input_path, "r", encoding="utf-8") as f:
        data_def = json.load(f)

    generated_code = generate_code_from_definition(data_def, template_path=template_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"Sukces! Wygenerowano plik {output_path} dla struktury {list(data_def.keys())[0]}.")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator kodu protokołu z pliku JSON")
    parser.add_argument("--input", default="interface.json", help="Ścieżka do pliku JSON")
    parser.add_argument("--output", default="protocol.py", help="Ścieżka do pliku wyjściowego")
    parser.add_argument("--template", default="template.j2", help="Ścieżka do szablonu Jinja")
    args = parser.parse_args()
    generate_code(args.input, args.output, args.template)

from typing import Dict 

def read_file(path: str) -> str:
    file = open(path, "r")
    content = file.read()
    file.close()
    return content

def write_file(path: str, content: str) -> None:
    file = open(path, "w")
    file.write(content)
    file.close()

def generate_world(main_file: str, output_path: str, include_map: Dict[str, str], replace_map: Dict[str, str]) -> None:
    main_content = read_file(main_file)

    for incl_str, path in include_map.items():
        content = read_file(path)

        for old_str, new_str in replace_map.items():
            content = content.replace(old_str, new_str)

        main_content = main_content.replace(incl_str, content)

    write_file(output_path, main_content)

if __name__ == "__main__":
    pass

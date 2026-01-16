def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    else:
        print("Error: Unable to read file with supported encodings.")
        return []

    # Skip header and empty lines
    for line in lines[1:]:
        line = line.strip()
        if line:
            raw_lines.append(line)

    return raw_lines

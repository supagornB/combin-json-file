import json
import os.path
import codecs

path_input = "input_file/"
path_output = "output_file/"
filename_output = "final.json"

def merge_duplicate_key(main: dict, data: dict):
    for k, v in data.items():
        if not main.get(k):
            main[k] = v

        if type(v) != type(main[k]):
            new_key = f"{k}_{type(v).__name__}"
            main[new_key] = v
        elif type(v) is dict:
            main[k] = merge_duplicate_key(main[k], v)
        elif type(v) is list:
            main[k] = expand_list(main[k], v)
    return main

def expand_list(list_main: list, list_data: list):
    try:
        count_main = len(list_main)
        count_data = len(list_data)
        max_loop = max(len(list_main), len(list_data))
        for idx in range(max_loop):
            if idx > count_main and idx < count_data:
                list_main.append(list_data[idx])
                continue
            elif idx > count_data:
                break

            for data in list_data:
                list_main[idx] = merge_duplicate_key(list_main[idx], data)
    except Exception as e:
        print(f"Error: {e}")
    return list_main

def main():
    data_final = dict()
    try:
        filename_list = os.listdir(path_input)
        if not filename_list:
            return "No file json."

        for idx, filename in enumerate(filename_list):
            print(f"filename: {filename}")
            if filename.split(".")[-1] != "json":
                print(f"{filename} is not JSON file.")
                continue
            in_filepath = path_input + filename
            data = json.load(open(in_filepath, encoding="utf-8"))
            if not idx:
                data_final = data
                continue
            data_final = merge_duplicate_key(data_final, data)
        
        out_filepath = path_output + filename_output
        with open(out_filepath, "w", encoding='utf-8') as json_file:
            json.dump(data_final, json_file, indent=4, ensure_ascii=False)
            print("Combin success.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()






# coding: utf-8

import argparse
import datetime
import pandas as pd

DEFAULT_LIMIT_SIZE_MB = 150
DEFAULT_SIDE = 'b'

argparser = argparse.ArgumentParser()
argparser.add_argument('--table-name', '-t', type=str, default='mvp_downloader_library',
                       help="Name of the table to insert into. Default is 'mvp_downloader_library_beta'.")
argparser.add_argument('--default-side', '-s', type=str, choices=['b', 'c'], default=None,
                       help="Default side to choose when both sides have valid different sizes. If not set, will prompt user.")
argparser.add_argument('--limit-size-mb', '-l', type=int, default=DEFAULT_LIMIT_SIZE_MB,
                       help=f"Limit size in MB to consider a size valid. Default is {DEFAULT_LIMIT_SIZE_MB} MB.")
args = argparser.parse_args()

limit_size = args.limit_size_mb * 1024 * 1024

df_b = pd.read_csv('mvp_downloader_library_20251107_broija.csv')
df_c = pd.read_csv('mvp_downloader_library_20251107_ceypey.csv')

# Merge the two DataFrames on 'id' to compare them side by side
df_merged = pd.merge(df_b, df_c, on='id', how='outer', suffixes=('_b', '_c')).sort_index()

resolved = []
output_columns = df_b.columns.tolist()

# Size is valid if it is a positive number but not exceeding limit_size
def is_valid_size(size):
    return pd.notna(size) and size > 0 and size <= limit_size

# Extract row data based on side, either 'b' or 'c'
def get_row_from_side(row, side):
    result = {}
    for col in output_columns:
        if col == 'id':
            result[col] = row['id']
        else:
            value = row[f"{col}_{side}"]
            if pd.notna(value) and type(value) == float:
                value = int(value)
            result[col] = value

    return result

for index, row in df_merged.iterrows():
    size_b = row['deeplink_file_size_b']
    size_c = row['deeplink_file_size_c']
    valid_b = is_valid_size(size_b)
    valid_c = is_valid_size(size_c)

    if valid_b and not valid_c: # Only side b is valid
        resolved.append(get_row_from_side(row, 'b'))
    elif not valid_b and valid_c: # Only side c is valid
        resolved.append(get_row_from_side(row, 'c'))
    elif valid_b and valid_c and size_b != size_c:
        print(f"Both sides have valid different sizes for id {row['id']}: {size_b} (b), {size_c} (c)")
        if DEFAULT_SIDE is not None:
            print(f"Defaulting to side {DEFAULT_SIDE}.")
            resolved.append(get_row_from_side(row, DEFAULT_SIDE))
        else:
            print("Which one do you want to keep? (b/c): ", end='')
            
            choice = None
            first_iteration = True
            while choice not in ['b', 'c']:
                if not first_iteration:
                    print("Invalid choice. Please enter 'b' or 'c': ", end='')
                else:
                    first_iteration = False
                choice = input().strip().lower()
            if choice == 'b':
                resolved.append(get_row_from_side(row, 'b'))
            elif choice == 'c':
                resolved.append(get_row_from_side(row, 'c'))

# Convert output list to DataFrame
df_resolved = pd.DataFrame(resolved, columns=output_columns)

# Summing up sizes
total_size = df_resolved['deeplink_file_size'].sum()
total_size_gb = total_size / (1024 ** 3)

print(f"Total deeplink_file_size: {total_size} bytes ({total_size_gb:.2f} GB)")

# -- Create SQL --

sql_lines = ["-- Generated SQL script"]
## TRUNCATE
sql_lines.append(f"TRUNCATE TABLE {args.table_name};")

## INSERTS
sql_lines.append(f"INSERT INTO {args.table_name} ({', '.join(output_columns)}) VALUES")

last_index = len(df_resolved) -1
for index, row in df_resolved.iterrows():
    values = []
    for col in output_columns:
        val = row[col]
        if pd.isna(val):
            values.append("NULL")
        elif isinstance(val, str):
            escaped_val = val.replace("'", "''")
            values.append(f"'{escaped_val}'")
        elif isinstance(val, float):
            values.append(str(int(val)))
        else:
            values.append(str(val))
    sql_line = f"  ({', '.join(values)})"
    if index < last_index:
        sql_line += ","
    sql_lines.append(sql_line)

# Write to output SQL file
file_date = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_sql_file = f'02_fill_mvp_downloader_library_insert_{file_date}.sql'

with open(output_sql_file, 'w', encoding='utf-8') as f:
    f.write("\n".join(sql_lines))

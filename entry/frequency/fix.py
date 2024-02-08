# Define the paths for the input and output files
input_file_path = 'jp_word_to_freq.csv'
output_file_path = 'jp_word_to_freq2.csv'

# Open the input file for reading and the output file for writing
with open(input_file_path, 'r', encoding='utf-8') as input_file, \
        open(output_file_path, 'w', encoding='utf-8') as output_file:
    # Iterate over each line in the input file
    for line in input_file:
        # Replace tabs with commas and remove '_x000D_'
        corrected_line = line.replace('\t', ',').replace('_x000D_', '').strip()
        # Write the corrected line to the output file
        output_file.write(corrected_line + '\n')

print(f'Fixed file saved to {output_file_path}')

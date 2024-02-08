
# Open the CSV file
with open('jp_word_to_freq.csv', 'r') as file:
    # Read the CSV data
    csv_data = file.read()

# Split the data into lines
lines = csv_data.strip().split('\n')

# Extract the first and last element from each line
extracted_words = [line.split(',')[0] for line in lines]

extracted_word_freqs = [line.split(',')[-1] for line in lines]

print(extracted_words)
print(extracted_word_freqs)

# lines = csv_data.strip().split('\n')

# # Extract the first and last element from each line
# extracted_elements = [(line.split(',')[0], line.split(',')[-1])
#                       for line in lines]

# print(extracted_elements)

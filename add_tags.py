import os

# Define the directory containing the markdown files
directory = r'C:\Users\Dan\Desktop\The Anitalmid Project\The Anitalmid Project'

# Define keywords and corresponding tags
keywords_to_tags = {
    'leadership': 'leadership',
    'teamwork': 'teamwork',
    'sales': 'sales',
    'software': 'software',
    'management': 'management',
    'communication': 'communication',
    'project': 'project',
}

def add_tags_to_markdown_files(directory):
    print("Starting to process markdown files...")
    
    try:
        files = os.listdir(directory)
        print(f'Files in directory: {files}')  # Show files in the directory
    except Exception as e:
        print(f'Error accessing directory {directory}: {e}')
        return
    
    for filename in files:
        if filename.endswith('.md'):
            print(f'Processing file: {filename}')
            file_path = os.path.join(directory, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.readlines()
                print(f'Content read successfully from {filename}')
            except Exception as e:
                print(f'Error reading {file_path}: {e}')
                continue
            
            existing_tags = []
            frontmatter_end = False
            
            # Check for existing tags in frontmatter
            for i, line in enumerate(content):
                if line.startswith('---'):
                    if frontmatter_end:
                        break  # Exit if we already passed the end of frontmatter
                    frontmatter_end = True
                    continue
                
                if frontmatter_end:
                    if line.startswith('tags:'):
                        existing_tags = line.strip().split(': ')[1].strip('[]').split(', ')
                        print(f'Existing tags found: {existing_tags}')
                        break
            
            # Create a set for unique tags
            tags = set(existing_tags)
            
            # Scan for keywords and add corresponding tags
            for line in content:
                for keyword, tag in keywords_to_tags.items():
                    if keyword.lower() in line.lower():
                        tags.add(tag)
                        print(f'Added tag: {tag} for keyword: {keyword}')
            
            # Prepare the new tags line; remove empty entries and format correctly
            tags = list(filter(None, tags))  # Remove empty entries
            new_tags_line = f'tags: [{", ".join(tags)}]'
            print(f'New tags line to write: {new_tags_line}')
            
            # Update the markdown file with new tags
            if frontmatter_end:
                for i, line in enumerate(content):
                    if line.startswith('tags:'):
                        content[i] = new_tags_line + '\n'
                        print(f'Updating the tags line in {filename}')
                        break
                
                try:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(content)
                    print(f'Updated tags in {filename}')
                except Exception as e:
                    print(f'Error writing to {file_path}: {e}')
            else:
                print(f'No frontmatter found in {filename}. Skipping...')

# Run the function
if __name__ == "__main__":
    add_tags_to_markdown_files(directory)

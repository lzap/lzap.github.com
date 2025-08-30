#!/usr/bin/python

import os
import re
import csv
import yaml

def generate_cloudflare_redirects(content_dir="content", output_file="redirects.csv"):
    """
    Walks through the Hugo content directory, finds posts with aliases, and generates a
    Cloudflare bulk redirect CSV file without using external dependencies like frontmatter.

    Args:
        content_dir (str): The path to the Hugo content directory.
        output_file (str): The name of the output CSV file.
    """
    redirects = []

    # Cloudflare CSV headers
    redirects.append(["source_url", "target_url", "status"])

    # Regex to extract the permalink from the file path
    # Assumes a common Hugo permalink structure like /posts/YYYY/post-name/
    permalink_regex = re.compile(r"content/posts/(\d{4})/(.+)\.md")

    print(f"Searching for aliases in '{content_dir}'...")

    for root, dirs, files in os.walk(content_dir):
        for file in files:
            # Only process markdown files
            if file.endswith((".md", ".adoc")):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                        # Use a regex to find the YAML front matter block
                        match = re.search(r'---\s*\n(.*?)\n---', content, re.DOTALL)

                        if match:
                            front_matter_str = match.group(1)

                            # Safely load the YAML content
                            front_matter = yaml.safe_load(front_matter_str)

                            if front_matter and "aliases" in front_matter and front_matter["aliases"]:
                                aliases = front_matter["aliases"]

                                # Extract permalink from file path
                                permalink_match = permalink_regex.search(file_path.replace(os.sep, '/'))
                                if permalink_match:
                                    year = permalink_match.group(1)
                                    slug = os.path.splitext(permalink_match.group(2))[0]
                                    permalink = f"/posts/{year}/{slug}/"

                                    for alias in aliases:
                                        redirects.append([alias, permalink, "301"])
                                        print(f"Found alias: {alias} -> {permalink}")
                                else:
                                    print(f"Warning: Could not determine permalink for {file_path}")
                        else:
                             print(f"Warning: No valid front matter found in {file_path}")

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    if not redirects:
        print("No aliases found. No CSV file will be generated.")
        return

    # Write the redirects to a CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows(redirects)

    print(f"\nSuccessfully generated {len(redirects) - 1} redirects.")
    print(f"CSV file '{output_file}' created for Cloudflare bulk redirects.")
    print("Remember to remove the aliases from your Hugo content and submit the redirects.csv file to Cloudflare.")

if __name__ == "__main__":
    # Ensure the 'pyyaml' library is installed: pip install pyyaml
    try:
        import yaml
    except ImportError:
        print("The 'pyyaml' library is not installed.")
        print("Please install it with: pip install pyyaml")
    else:
        generate_cloudflare_redirects()

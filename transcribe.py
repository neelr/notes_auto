from pathlib import Path
import sys
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

# Ensure an API key is set for OpenAI


def read_file(file_path):
    """Reads the content of a file and returns it."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)


def send_to_chatgpt(content):
    """Sends content to ChatGPT in chunks and returns the LaTeX conversion of the combined notes."""
    try:
        # Split the content into chunks of approximately 2000 words
        words = content.split()
        chunk_size = 2000
        chunks = [words[i:i+chunk_size]
                  for i in range(0, len(words), chunk_size)]

        combined_notes = ""
        print(
            f"Generating lecture notes in chunks, {len(chunks)} chunks total.")

        for chunk in chunks:
            print(f"Generating notes for chunk {chunks.index(chunk)+1}...")
            non_latex = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a technical note assistant."},
                    {
                        "role": "user",
                        "content": f"""
                        here are 2000 words of a lecture transcript:
                        {chunk}

                        - turn this into lecture notes—_USE PARAGRAPHS of text while using bullet points sparingly and for organization_.
                        - use bolding, italics, and other formatting to make it look nice.
                        - include all code blocks and math equations in latex.
                        - make it extremely technical and lengthy
                        - examples
                            - ex. if positive feedback loops are mentioned, give an example of ripe fruit ripening faster in a bowl.
                            - ex. if grep is mentioned, write out `grep -r "search term" .` and explain what it does.
                            - ex. if row echelon form is mentioned, write out a latex matrix (\begin matrix 1 & 0 & 0 \\ \end) and show the steps to get to row echelon form."""
                    }
                ]
            )

            non_latex_content = non_latex.choices[0].message.content.strip()
            combined_notes += "\n" + non_latex_content

        print("Converting combined notes to LaTeX...")
        # Convert the combined notes to LaTeX
        latex_conversion_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a technical converter assistant."},
                {
                    "role": "user",
                    "content": f"""
                    {combined_notes}

                    remove extremely redundant lists, but do so extremely sparingly (ie. make it readable)
                    convert the above to latex lecture note paper—make it aesthethically pleasing. only output the latex (do conversions from markdown to latex bolding, url, italics, etc.), no code block or extra text and it should compile standalone (use hyperref table of contents though).\n\n"""}
            ]
        )

        # Extract the LaTeX conversion response text
        latex = latex_conversion_response.choices[0].message.content.strip()

        return latex
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        sys.exit(1)


def save_to_file(content, file_path):
    """Saves content to a file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py arg1.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = Path(input_file).stem + ".tex"

    file_content = read_file(input_file)
    latex_content = send_to_chatgpt(file_content)
    save_to_file(latex_content, output_file)

    print(f"Output saved to {output_file}")

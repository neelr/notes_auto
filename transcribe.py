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
    """Sends content to ChatGPT and returns the LaTeX conversion."""
    try:
        print("Generating lecture notes...")
        non_latex = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""

                    actual transcript to convert to notes:
                    {content}

                    - *INCLUDE ALL LECTURE EXAMPLES* OR create your own. make sure it is clear and easy & formatted well
                        - ex. if positive feedback loops are mentioned, give an example of ripe fruit ripening faster in a bowl.
                        - ex. if grep is mentioned, explain how to use it and give an example of how to search for a string in a file + what the output looks like.
                        - ex. if row echelon form is mentioned, give an example of converting a matrix to row echelon form.
                    - EXPAND AND INCLUDE ON DEFINITIONS, EXAMPLES, AND DETAILS IN YOUR NOTES—especially for uncommon terms or concepts (assume no prior knowledge).
                       - the length of the note should be proportional to how long the topic was discussed in the lecture.
                    - 3000 words long—longer is better than shorter, should be proportional to the length of the lecture.
                    - bold key terms & use bullet points with paragraphs between chunks.

                    write out a good professor full lecture notes for a student 2nd person include all details (feel free to include steps, ie. fill in steps/explain algorithms like A* or Existentialism or Gaussian methods if mentioned + details from your own knowledge) and include minute tips that might help people studying. Feel free to include paragraphs and annotate (bold/italics) accordingly. Structure it well with subsections, bullets, and content. \n\n.\n\n"""}
            ]
        )

        non_latex_content = non_latex.choices[0].message.content.strip()

        print("Converting to LaTeX...")
        # Continue the conversation with LaTeX conversion, without including the original lecture transcript
        latex_conversion_response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""now convert it to a full latex document with a table of contents. only output the latex (do conversions from markdown to latex bolding, url, italics, etc.), no code block or extra text and it should compile standalone (use hyperref though).\n\n{
                        non_latex_content}"""}
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

from PyPDF2 import PdfReader, PdfWriter
import os

# Define input and output paths
input_path = r"S:\ITS\Pipeline Integrity\Cathodic Protection\Districts\Deep Basin\2018\AnnualSurvey\NEBC Gathering  2018 CP Compliance Survey\Plateau NEBC Gathering Report 18(JD).pdf"
# Define output directory in Downloads folder
output_dir = os.path.join(os.path.expanduser("~"), "Downloads", "Extracted_Pages")
os.makedirs(output_dir, exist_ok=True)


# Define the page range
start_page = 41  # 0-indexed, so 36 corresponds to page 37
end_page = 52    # Up to page 52

reader = PdfReader(input_path)

for i in range(start_page, end_page):
    writer = PdfWriter()
    writer.add_page(reader.pages[i])

    # Option to manually name the file
    new_name = input(f"Enter a name for page {i+1}: ")  # Add 1 for human-readable index
    output_path = os.path.join(output_dir, f"{new_name}.pdf")

    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

print(f"Pages {start_page+1} to {end_page} have been saved in {output_dir}")

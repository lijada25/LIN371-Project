import os
import glob

# -----------------------------
# This script processes .cha files in the input directory,
# converting @G: Cinderella sections to @BG: Cinderella and @EG: Cinderella format,
# and saves the modified files in the output directory.
# -----------------------------

input_dir = "/Users/jadali/Documents/AphasiaBank Final dataset/Final dataset" # replace with your local dir.
output_dir = "/Users/jadali/Documents/AphasiaBank Final dataset/Cinderella"

# -----------------------------
# Create output folder if it doesn't exist
# -----------------------------
os.makedirs(output_dir, exist_ok=True)

def get_task_name(line):
    if line.startswith("@G:"):
        return line.replace("@G:", "").strip()
    return None

# -----------------------------
# convert @G: Cinderella sections to @BG: Cinderella and @EG: Cinderella format,
# effectively isolated the Cinderella task from the rest of the transcript.
# -----------------------------
def convert_g_to_bg_eg(lines):
    new_lines = []
    inside_cinderella = False

    for line in lines:
        stripped = line.strip()
        task = get_task_name(stripped)

        # Start Cinderella
        if task == "Cinderella":
            new_lines.append("@BG:	Cinderella\n")
            inside_cinderella = True
            continue

        # If new task starts → close Cinderella

        if inside_cinderella and task is not None and task != "Cinderella":
            new_lines.append("@EG:	Cinderella\n")
            break
            # inside_cinderella = False

        if inside_cinderella:
            new_lines.append(line)

    # If file ends while still inside Cinderella
    if inside_cinderella and (len(new_lines) == 0 or not new_lines[-1].startswith("@EG:")):
        new_lines.append("@EG:	Cinderella\n")

    return new_lines

# -----------------------------
# Process all .cha files
# -----------------------------
for filepath in glob.glob(os.path.join(input_dir, "*.cha")):
    with open(filepath, "r") as f:
        lines = f.readlines()

    fixed_lines = convert_g_to_bg_eg(lines)

    filename = os.path.basename(filepath)
    output_path = os.path.join(output_dir, filename)

    with open(output_path, "w") as f:
        f.writelines(fixed_lines)

    print(f"Processed: {filename}")
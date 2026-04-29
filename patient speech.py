import os
import glob
import re

# -----------------------------
# This script processes the Cinderella dataset from AphasiaBank,
# extracting patient speech and creating two versions of the text:
# -----------------------------

input_dir = "/Users/jadali/Documents/AphasiaBank Final dataset/cinderella dataset" # replace path with your local dir.
out_plain = "/Users/jadali/Documents/AphasiaBank Final dataset/plaintext"
out_clinical = "/Users/jadali/Documents/AphasiaBank Final dataset/clinical"

os.makedirs(out_plain, exist_ok=True)
os.makedirs(out_clinical, exist_ok=True)

# -----------------------------
# Clean text by removing CLAN annotations and artifacts
# -----------------------------
def clean_text(text, aggressive=False):
    # remove MOR/GRA artifacts if still present
    text = re.sub(r"%mor:.*", "", text)
    text = re.sub(r"%gra:.*", "", text)

    # remove timestamps
    text = re.sub(r"•.*?•", "", text)

    # remove bracketed glosses [: Cinderella]
    text = re.sub(r"\[:.*?\]", "", text)

    # remove CLAN repairs / codes
    text = re.sub(r"\[\*.*?\]", "", text)
    text = re.sub(r"\[//\]|\[/\]", "", text)

    # remove discourse markers like [+ exc]
    text = re.sub(r"\[\+.*?\]", "", text)

    # remove gesture annotations &=ges:face
    text = re.sub(r"&=[^\s]+", "", text)

    # remove word-level codes (Cinderella@u → Cinderella)
    text = re.sub(r"@\w+", "", text)

    # normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # optional aggressive cleanup (for embeddings)
    if aggressive:
        text = re.sub(r"[^a-zA-Z\s']", "", text)
        text = re.sub(r"\s+", " ", text).strip()

    return text

# -----------------------------
# Extract *PAR lines which contain patient speech
# -----------------------------
def extract_par(lines):
    par_text = []

    for line in lines:
        line = line.strip()

        if line.startswith("*PAR:"):
            content = line.split(":", 1)[1]
            par_text.append(content)

    return par_text

# -----------------------------
# Process each .cha file in the input directory
# -----------------------------
for filepath in glob.glob(os.path.join(input_dir, "*.cha")):

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    par_lines = extract_par(lines)

    raw_text = " ".join(par_lines)

    # VERSION 1: clinical (keeps structure + disfluencies)
    clinical = clean_text(raw_text, aggressive=False)

    # VERSION 2: plaintext (ML / embeddings)
    plain = clean_text(raw_text, aggressive=True)

    fname = os.path.basename(filepath).replace(".cha", "")

    # save clinical
    with open(os.path.join(out_clinical, fname + "_clinical.txt"), "w", encoding="utf-8") as f:
        f.write(clinical)

    # save plaintext
    with open(os.path.join(out_plain, fname + "_plain.txt"), "w", encoding="utf-8") as f:
        f.write(plain)

    print(f"Processed {fname}")
def chunk_text(text, size=200):
    words = text.split()
    return [" ".join(words[i:i+size]) for i in range(0, len(words), size)]


def load_data(file_paths=["kr_vectorled.txt", "kamlesh_profile.txt"]):
    data = []

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as f:
            raw_blocks = f.read().split("\n\n")

        for block in raw_blocks:

            #  Instruction dataset
            if "Instruction:" in block and "Output:" in block:
                try:
                    instruction_part = block.split("Instruction:")[1].split("Output:")[0].strip()
                    output_part = block.split("Output:")[1].strip()

                    data.append({
                        "instruction": instruction_part,
                        "output": output_part,
                        "source": "dataset"
                    })
                except:
                    continue

            #  Profile data (chunk it if it's too long)
            else:
                if block.strip():
                    chunks = chunk_text(block.strip())

                    for chunk in chunks:
                        data.append({
                            "instruction": chunk,
                            "output": chunk,
                            "source": "profile"
                        })

    return data
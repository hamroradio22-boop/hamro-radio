
import subprocess
from pathlib import Path

OUTPUT_DIR = Path("audio")
OUTPUT_DIR.mkdir(exist_ok=True)

def make_voice(text, presenter="male", filename="announcement.wav"):
    if presenter not in ("male", "female"):
        raise ValueError("Presenter must be male or female")

    model = (
        "models/ne_NP-male.onnx"
        if presenter == "male"
        else "models/ne_NP-female.onnx"
    )

    output = OUTPUT_DIR / filename

    try:
        subprocess.run(
            [
                "piper",
                "--model", model,
                "--output_file", str(output)
            ],
            input=text,
            text=True,
            check=True
        )
        return str(output)

    except Exception as error:
        print("Voice generation error:", error)
        return None


if __name__ == "__main__":
    make_voice(
        "नमस्कार, तपाईं सुनिरहनुभएको छ हाम्रो रेडियो।",
        "male",
        "male_test.wav"
    )

    make_voice(
        "नमस्कार, तपाईं सबैलाई हार्दिक स्वागत छ।",
        "female",
        "female_test.wav"
    )

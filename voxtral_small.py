# voxtral_small_persian_asr.py
import torch
import torchaudio
from transformers import VoxtralForConditionalGeneration, AutoProcessor
import os
import subprocess
import time


class VoxtralSmallPersianASR:
    def __init__(self):
        """Initialize Voxtral Small 24B model for high-quality Persian ASR"""
        self.model_id = "mistralai/Voxtral-Small-24B-2507"
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")

        if self.device == "cuda":
            # Check VRAM availability for 24B model
            vram_total = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
            print(f"Available VRAM: {vram_total:.1f}GB")
            if vram_total < 24:
                print(f"Warning: Voxtral Small 24B typically needs 48GB+ VRAM")
                print(f"Your GPU has {vram_total:.1f}GB. Model will use CPU offloading.")

    def load_model(self):
        """Load Voxtral Small 24B model with optimal settings"""
        print(f"Loading {self.model_id}...")
        print("This may take 10-20 minutes for first download (24B parameters)")
        start_time = time.time()

        try:
            # Load processor
            print("Loading processor...")
            self.processor = AutoProcessor.from_pretrained(self.model_id)

            # Load model with appropriate settings for 24B parameters
            if self.device == "cuda":
                print("Loading model with GPU optimization...")
                self.model = VoxtralForConditionalGeneration.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.bfloat16,  # Best precision for large models
                    device_map="auto",  # Automatic device placement
                    low_cpu_mem_usage=True,
                    trust_remote_code=True,
                    offload_folder="./model_offload",  # Offload to disk if needed
                )

                # Clear cache
                torch.cuda.empty_cache()

                # Report VRAM usage
                vram_used = torch.cuda.memory_allocated() / 1024 ** 3
                vram_total = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
                print(f"VRAM usage: {vram_used:.1f}GB / {vram_total:.1f}GB")

            else:
                print("Loading model in CPU mode...")
                self.model = VoxtralForConditionalGeneration.from_pretrained(
                    self.model_id,
                    torch_dtype=torch.float32,
                    device_map="cpu",
                    low_cpu_mem_usage=True,
                    trust_remote_code=True,
                )

            load_time = time.time() - start_time
            print(f"Model loaded successfully in {load_time:.1f} seconds!")
            return True

        except torch.cuda.OutOfMemoryError:
            print("GPU out of memory. Trying CPU mode...")
            self.device = "cpu"
            return self.load_model()

        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def transcribe_persian(self, audio_path):
        """Transcribe Persian audio with high quality using Small model"""
        if self.model is None or self.processor is None:
            if not self.load_model():
                return None

        print("Processing Persian audio with Voxtral Small 24B...")
        start_time = time.time()

        # Try different Persian approaches
        approaches = [
            self.transcribe_chat_persian,
            self.transcribe_audio_only,
            self.transcribe_with_explicit_instruction
        ]

        for i, approach in enumerate(approaches, 1):
            try:
                print(f"Trying approach {i}/3...")
                result = approach(audio_path)
                if result and len(result.strip()) > 5:
                    process_time = time.time() - start_time
                    print(f"Success! Processing time: {process_time:.1f} seconds")
                    return result.strip()
                else:
                    print(f"Approach {i} gave empty/short result")
            except Exception as e:
                print(f"Approach {i} failed: {e}")
                continue

        return "All transcription approaches failed with Voxtral Small model"

    def transcribe_chat_persian(self, audio_path):
        """Chat-based Persian transcription with detailed instructions"""
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "audio", "path": audio_path},
                    {
                        "type": "text",
                        "text": "Please carefully transcribe this Persian/Farsi audio into accurate Persian text. Pay attention to proper Persian grammar and vocabulary. لطفا این صدای فارسی را با دقت و با رعایت دستور زبان فارسی رونویسی کنید."
                    },
                ],
            }
        ]

        # Process conversation
        inputs = self.processor.apply_chat_template(conversation)
        return self.generate_transcription(inputs)

    def transcribe_audio_only(self, audio_path):
        """Audio-only transcription to let model auto-detect Persian"""
        conversation = [
            {
                "role": "user",
                "content": [{"type": "audio", "path": audio_path}]
            }
        ]

        inputs = self.processor.apply_chat_template(conversation)
        return self.generate_transcription(inputs)

    def transcribe_with_explicit_instruction(self, audio_path):
        """Explicit Persian transcription instruction"""
        conversation = [
            {
                "role": "user",
                "content": [
                    {"type": "audio", "path": audio_path},
                    {
                        "type": "text",
                        "text": "Transcribe to Persian text only. فقط متن فارسی."
                    },
                ],
            }
        ]

        inputs = self.processor.apply_chat_template(conversation)
        return self.generate_transcription(inputs)

    def generate_transcription(self, inputs):
        """Generate transcription from processed inputs"""
        try:
            # Move to appropriate device and dtype
            if self.device == "cuda":
                inputs = inputs.to(self.device, dtype=torch.bfloat16)
            else:
                inputs = inputs.to(self.device, dtype=torch.float32)

            # Generate with optimized settings for transcription
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=1000,  # Longer for detailed Persian transcription
                    do_sample=False,  # Deterministic for accuracy
                    temperature=0.0,
                    pad_token_id=self.processor.tokenizer.eos_token_id,
                    repetition_penalty=1.1,  # Reduce repetitions
                )

            # Decode only the new tokens
            decoded_outputs = self.processor.batch_decode(
                outputs[:, inputs.input_ids.shape[1]:],
                skip_special_tokens=True
            )

            return decoded_outputs[0]

        except Exception as e:
            print(f"Generation failed: {e}")
            return None

    def batch_transcribe(self, audio_files):
        """Transcribe multiple Persian audio files"""
        results = {}

        print(f"Starting batch transcription of {len(audio_files)} files...")

        for i, audio_file in enumerate(audio_files, 1):
            print(f"\nProcessing file {i}/{len(audio_files)}: {audio_file}")

            if not os.path.exists(audio_file):
                print(f"File not found: {audio_file}")
                results[audio_file] = "File not found"
                continue

            # Convert to WAV if needed
            wav_file = audio_file.replace('.mp3', '_16k_mono.wav').replace('.m4a', '_16k_mono.wav')
            if convert_to_wav(audio_file, wav_file):
                result = self.transcribe_persian(wav_file)
                results[audio_file] = result if result else "Transcription failed"

                # Save individual result
                result_file = audio_file.replace('.mp3', '_transcription.txt').replace('.m4a', '_transcription.txt')
                with open(result_file, 'w', encoding='utf-8') as f:
                    f.write(results[audio_file])
                print(f"Saved to: {result_file}")
            else:
                results[audio_file] = "Audio conversion failed"

            # Clear memory between files
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        return results


def convert_to_wav(input_path, output_path):
    """Convert audio file to WAV format optimized for Voxtral"""
    if os.path.exists(output_path):
        print(f"WAV file already exists: {os.path.basename(output_path)}")
        return True

    print(f"Converting {os.path.basename(input_path)} to WAV...")
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000",  # 16kHz sample rate
        "-ac", "1",  # Mono
        "-c:a", "pcm_s16le",  # 16-bit PCM
        output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("Conversion successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion failed: {e}")
        return False


def main():
    # Configuration
    INPUT_AUDIO = "voice1.mp3"  # Your Persian audio file
    WAV_OUTPUT = "voice1_16k_mono.wav"

    print("Voxtral Small 24B Persian ASR - High Quality Transcription")
    print("=" * 70)
    print("Model: Voxtral-Small-24B-2507 (48GB+ VRAM recommended)")
    print("Language: Persian/Farsi optimized")
    print("Quality: Professional-grade transcription")
    print("=" * 70)

    # Check if input file exists
    if not os.path.exists(INPUT_AUDIO):
        print(f"Input file {INPUT_AUDIO} not found!")
        print("Please place your Persian audio file in the same directory.")
        return

    # Convert audio to required format
    if not convert_to_wav(INPUT_AUDIO, WAV_OUTPUT):
        print("Audio conversion failed!")
        return

    # Initialize ASR system
    asr = VoxtralSmallPersianASR()

    print(f"\nTranscribing Persian audio: {INPUT_AUDIO}")
    result = asr.transcribe_persian(WAV_OUTPUT)

    if result and "failed" not in result.lower():
        print("\n" + "=" * 70)
        print("HIGH-QUALITY PERSIAN TRANSCRIPTION:")
        print("=" * 70)
        print(result)
        print("=" * 70)

        # Save result
        output_file = "persian_transcription_small.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Result saved to: {output_file}")

        # Performance info
        if torch.cuda.is_available():
            final_vram = torch.cuda.memory_allocated() / 1024 ** 3
            print(f"Final VRAM usage: {final_vram:.1f}GB")

    else:
        print(f"Transcription result: {result}")

    # Optional: Batch processing example
    """
    # Uncomment for batch processing multiple files:
    audio_files = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]
    batch_results = asr.batch_transcribe(audio_files)
    print("Batch results:")
    for file, result in batch_results.items():
        print(f"{file}: {result[:100]}...")
    """


if __name__ == "__main__":
    print("Voxtral Small 24B - Professional Persian ASR")
    print("Requirements:")
    print("- 48GB+ VRAM recommended (will use CPU offloading if less)")
    print("- pip install torch torchaudio transformers librosa")
    print("- FFmpeg installed and in PATH")
    print("=" * 70)

    main()
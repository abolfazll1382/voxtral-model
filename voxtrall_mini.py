# voxtral_memory_optimized.py
import torch
import torchaudio
from transformers import VoxtralForConditionalGeneration, AutoProcessor
import os
import subprocess


class VoxtralPersianASR:
    def __init__(self, model_size="mini"):
        """Initialize Voxtral model optimized for GTX 1050 Ti 4GB VRAM"""
        self.model_id = "mistralai/Voxtral-Mini-3B-2507"
        self.processor = None
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")

    def load_model(self):
        """Load model with aggressive memory optimization for GTX 1050 Ti"""
        print(f"Loading {self.model_id} with memory optimization...")

        try:
            # Load processor first
            self.processor = AutoProcessor.from_pretrained(self.model_id)

            if self.device == "cuda":
                print("Using aggressive memory optimization for GTX 1050 Ti...")
                # Try loading with maximum memory efficiency
                self.model = VoxtralForConditionalGeneration.from_pretrained(
                    self.model_id,
                    dtype=torch.float16,  # Use float16 instead of bfloat16 to save memory
                    device_map="auto",
                    low_cpu_mem_usage=True,
                    torch_dtype=torch.float16,  # Ensure consistent dtype
                    offload_folder="./offload",  # Offload to disk if needed
                    offload_state_dict=True,
                )

                # Clear cache aggressively
                torch.cuda.empty_cache()

            else:
                self.model = VoxtralForConditionalGeneration.from_pretrained(
                    self.model_id,
                    dtype=torch.float32,
                    low_cpu_mem_usage=True
                )

            # Check actual VRAM usage
            if self.device == "cuda":
                vram_used = torch.cuda.memory_allocated() / 1024 ** 3
                vram_total = torch.cuda.get_device_properties(0).total_memory / 1024 ** 3
                print(f"VRAM usage: {vram_used:.1f}GB / {vram_total:.1f}GB")

                if vram_used > 3.5:  # Too much for GTX 1050 Ti
                    print("⚠️  Warning: High VRAM usage detected!")
                    print("🔄 Switching to CPU mode for better performance...")
                    del self.model
                    torch.cuda.empty_cache()
                    self.device = "cpu"
                    return self.load_model()  # Retry with CPU

            print("Model loaded successfully!")
            return True

        except torch.cuda.OutOfMemoryError:
            print("❌ GPU out of memory! Switching to CPU...")
            self.device = "cpu"
            return self.load_model()

        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    def transcribe_persian(self, audio_path):
        """Transcribe Persian audio using available methods"""
        if self.model is None or self.processor is None:
            if not self.load_model():
                return None

        print("Processing Persian audio...")

        # Check which methods are available
        available_methods = [method for method in dir(self.processor) if 'transcr' in method.lower()]
        print(f"Available transcription methods: {available_methods}")

        # Try the correct method name from your version
        transcription_methods = [
            'apply_transcrition_request',  # Official docs (with typo)
            'apply_transcription_request',  # Correct spelling
            'transcribe',
            'process_audio'
        ]

        for method_name in transcription_methods:
            if hasattr(self.processor, method_name):
                print(f"Found method: {method_name}")
                try:
                    method = getattr(self.processor, method_name)

                    if method_name in ['apply_transcrition_request', 'apply_transcription_request']:
                        # Try transcription mode
                        for lang in ["fa", "persian", "farsi"]:
                            try:
                                print(f"Trying {method_name} with language: {lang}")
                                inputs = method(
                                    language=lang,
                                    audio=audio_path,
                                    model_id=self.model_id
                                )

                                if inputs:
                                    return self.generate_from_inputs(inputs)

                            except Exception as e:
                                print(f"Language {lang} failed: {e}")
                                continue

                except Exception as e:
                    print(f"Method {method_name} failed: {e}")
                    continue

        # Fallback to chat mode
        return self.transcribe_chat_mode(audio_path)

    def generate_from_inputs(self, inputs):
        """Generate transcription from processed inputs"""
        try:
            # Move to device with appropriate dtype
            if self.device == "cuda":
                inputs = inputs.to(self.device, dtype=torch.float16)
            else:
                inputs = inputs.to(self.device, dtype=torch.float32)

            # Generate with memory optimization
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=300,  # Reduced to save memory
                    do_sample=False,
                    pad_token_id=self.processor.tokenizer.eos_token_id
                )

            # Decode only new tokens
            decoded_outputs = self.processor.batch_decode(
                outputs[:, inputs.input_ids.shape[1]:],
                skip_special_tokens=True
            )

            result = decoded_outputs[0].strip()
            return result if result else "Empty transcription result"

        except Exception as e:
            print(f"Generation failed: {e}")
            return None

    def transcribe_chat_mode(self, audio_path):
        """Use chat mode for Persian transcription"""
        print("Trying chat mode for Persian transcription...")

        try:
            # Simple conversation for transcription
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {"type": "audio", "path": audio_path},
                        {"type": "text", "text": "Transcribe this Persian audio. لطفا این صدا را رونویسی کنید."},
                    ],
                }
            ]

            # Process conversation
            inputs = self.processor.apply_chat_template(conversation)

            return self.generate_from_inputs(inputs)

        except Exception as e:
            print(f"Chat mode failed: {e}")
            return self.try_audio_only(audio_path)

    def try_audio_only(self, audio_path):
        """Try processing audio alone"""
        print("Trying audio-only processing...")

        try:
            conversation = [
                {
                    "role": "user",
                    "content": [{"type": "audio", "path": audio_path}]
                }
            ]

            inputs = self.processor.apply_chat_template(conversation)
            result = self.generate_from_inputs(inputs)

            return result if result else f"Model functional but no transcription. Methods available: {[m for m in dir(self.processor) if not m.startswith('_')][:5]}"

        except Exception as e:
            print(f"Audio-only failed: {e}")
            return f"All methods attempted. VRAM: {torch.cuda.memory_allocated() / 1024 ** 3 if torch.cuda.is_available() else 0:.1f}GB. Error: {e}"


def convert_to_wav(input_path, output_path):
    """Convert audio file to WAV format"""
    if os.path.exists(output_path):
        print(f"WAV file already exists: {output_path}")
        return True

    print(f"Converting {input_path} to WAV...")
    cmd = [
        "ffmpeg", "-y", "-i", input_path,
        "-ar", "16000", "-ac", "1",
        "-c:a", "pcm_s16le", output_path
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("Conversion successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg conversion failed: {e}")
        return False


def main():
    INPUT_AUDIO = "voice1.mp3"
    WAV_OUTPUT = "voice1_16k_mono.wav"

    print("Voxtral Persian ASR - Memory Optimized for GTX 1050 Ti")
    print("=" * 65)
    print("Hardware: GTX 1050 Ti (4GB VRAM limit)")
    print("Optimization: Aggressive memory management + CPU fallback")
    print("=" * 65)

    if not os.path.exists(INPUT_AUDIO):
        print(f"Input file {INPUT_AUDIO} not found!")
        return

    if not convert_to_wav(INPUT_AUDIO, WAV_OUTPUT):
        return

    asr = VoxtralPersianASR()

    print("\nTesting Persian transcription...")
    result = asr.transcribe_persian(WAV_OUTPUT)

    if result:
        print("\n" + "=" * 65)
        print("Persian Transcription Result:")
        print("=" * 65)
        print(result)
        print("=" * 65)

        with open("persian_transcription.txt", "w", encoding="utf-8") as f:
            f.write(result)
        print("💾 Result saved to persian_transcription.txt")

        if torch.cuda.is_available():
            final_vram = torch.cuda.memory_allocated() / 1024 ** 3
            print(f"📊 Final VRAM usage: {final_vram:.1f}GB")
            if final_vram > 3.5:
                print("⚠️  Consider using CPU mode for this model size")


if __name__ == "__main__":
    print("Memory-optimized Voxtral for 4GB VRAM systems")
    print("Install: pip install librosa")
    print("=" * 65)
    main()
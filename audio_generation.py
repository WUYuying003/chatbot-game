import torch
import numpy as np
from diffusers import AudioLDM2Pipeline, DPMSolverMultistepScheduler
import pyaudio
import scipy.io.wavfile as wav
import tempfile
import os

print("🎵 Loading AudioLDM2 model... This may take a while on first run.")

# Use CPU since we're on macOS without CUDA
device = "cpu"
torch_dtype = torch.float32  # Use float32 for CPU

pipeline = AudioLDM2Pipeline.from_pretrained(
    "cvssp/audioldm2-music", 
    torch_dtype=torch_dtype
)
pipeline.to(device)
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
    pipeline.scheduler.config
)

print("✅ Model loaded successfully!")

# Set up audio playback
p = pyaudio.PyAudio()

def play_audio(audio_array, sample_rate=16000):
    """Play audio array through speakers"""
    stream = p.open(
        format=pyaudio.paFloat32, 
        channels=1, 
        rate=sample_rate, 
        output=True
    )
    
    # Normalize audio to prevent clipping
    audio_normalized = np.clip(audio_array, -1.0, 1.0)
    
    # Convert to bytes and play
    audio_bytes = audio_normalized.astype(np.float32).tobytes()
    stream.write(audio_bytes)
    stream.stop_stream()
    stream.close()

try:
    while True:
        prompt = input("\n🎼 Give me a song description (or 'quit' to exit): ")
        
        if prompt.lower() in ['quit', 'exit', 'q']:
            break
            
        print(f"🎵 Generating audio for: '{prompt}'")
        print("⏳ This may take several minutes on CPU...")
        
        # Generate audio with reduced parameters for CPU
        audios = pipeline(
            prompt, 
            num_inference_steps=50,  # Reduced from 200 for faster generation
            audio_length_in_s=10,   # Reduced from 60 for faster generation
            guidance_scale=2.5      # Default guidance scale
        ).audios
        
        print("✅ Audio generated! Playing...")
        
        # Play the generated audio
        for i, audio in enumerate(audios):
            print(f"🔊 Playing audio {i+1}/{len(audios)}")
            play_audio(audio)
            
            # Also save to file
            temp_file = f"generated_audio_{i+1}.wav"
            wav.write(temp_file, 16000, (audio * 32767).astype(np.int16))
            print(f"💾 Saved as: {temp_file}")

except KeyboardInterrupt:
    print("\n🛑 Stopped by user")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    p.terminate()
    print("👋 Goodbye!")
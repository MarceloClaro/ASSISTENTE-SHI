#!/usr/bin/env python
"""Test audio output devices"""
import sounddevice as sd

print("=" * 60)
print("DISPOSITIVOS DE SAÍDA DE ÁUDIO DISPONÍVEIS")
print("=" * 60)

for i in range(len(sd.query_devices())):
    dev = sd.query_devices(i)
    if dev['max_output_channels'] > 0:
        is_default = sd.default.device[1] == i
        marker = "✓ DEFAULT" if is_default else ""
        print(f"\n{i}: {dev['name']}")
        print(f"   Canais: {dev['max_output_channels']}")
        print(f"   Taxa de amostragem: {int(dev['default_samplerate'])}Hz")
        print(f"   {marker}")

print("\n" + "=" * 60)
print(f"Dispositivo padrão de saída: {sd.default.device[1]}")
print("=" * 60)

from src.physics.forcefield import ForceField

ff = ForceField()

print()

print("="*40)

print("FORCE FIELD")

print("="*40)

print()

for k,v in ff.__dict__.items():

    print(f"{k:15s}",v)

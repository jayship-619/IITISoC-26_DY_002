from src.io.xyz_reader import XYZReader

reader = XYZReader(
    "data/packed/network_packed.xyz"
)

xyz = reader.read()

print()

print("Atoms :", len(xyz))

print("First atom")

print(xyz[0])

print()

print("Last atom")

print(xyz[-1])

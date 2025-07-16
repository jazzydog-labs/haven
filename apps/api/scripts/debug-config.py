#!/usr/bin/env python3
"""Debug configuration loading."""

import os

from hydra import compose, initialize_config_dir
from hydra.core.global_hydra import GlobalHydra
from omegaconf import OmegaConf

# Set env vars
os.environ["DB_HOST"] = "localhost"
os.environ["DB_PORT"] = "5432"
os.environ["DB_NAME"] = "haven"
os.environ["DB_USER"] = "haven"
os.environ["DB_PASSWORD"] = "haven"

# Clear any existing Hydra instance
if GlobalHydra.instance().is_initialized():
    GlobalHydra.instance().clear()

# Initialize Hydra with config directory
initialize_config_dir(config_dir="/Users/paul/dev/jazzydog-labs/haven/conf", version_base="1.3")

# Compose configuration
cfg = compose(config_name="config")

# Print the full configuration
print("Full configuration:")
print(OmegaConf.to_yaml(cfg))

# Check what's in database section
print("\nDatabase section:")
if "database" in cfg:
    print(OmegaConf.to_yaml(cfg.database))
else:
    print("No database section found!")

# Print all top-level keys
print("\nTop-level keys:", list(cfg.keys()))

#!/usr/bin/env python3
"""
Configuration Validation Utility
Validates config.yaml without running the application
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import logging
logging.basicConfig(
    level=logging.WARNING,  # Only show warnings and errors
    format='%(levelname)s: %(message)s'
)

from config import load_config


def main():
    """Validate configuration file"""
    print("=" * 50)
    print("Pixel Plant - Configuration Validator")
    print("=" * 50)
    print()

    try:
        # Load and validate
        config = load_config()

        # Show validation report
        print(config.get_validation_report())
        print()

        # Show loaded configuration
        if config._validation_warnings:
            print("\n⚠️  Configuration loaded with warnings")
            print("Review warnings above and update config/config.yaml if needed")
            return 0
        else:
            print("\n✅ Configuration is valid and ready to use!")
            return 0

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("\nMake sure config/config.yaml exists")
        return 1

    except ValueError as e:
        print(f"❌ Configuration validation failed!\n")
        print(str(e))
        print("\nPlease fix the errors in config/config.yaml")
        return 1

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Learning Insights Generator
Generates and displays insights from learned patterns
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import logging
logging.basicConfig(level=logging.WARNING)

from config import get_config
from ai import PatternLearner


def main():
    """Generate insights report"""
    print("=" * 60)
    print("Pixel Plant - Learning Insights Generator")
    print("=" * 60)
    print()

    try:
        # Load config
        config = get_config()

        # Create pattern learner
        learner = PatternLearner(
            data_directory=config.system.data_directory,
            learning_enabled=True,
            pattern_window_days=config.behavior.pattern_window_days
        )

        # Check if there's data
        summary = learner.get_learning_summary()

        if summary['total_activities_logged'] == 0:
            print("⚠️  No learning data found yet.")
            print("\nThe Pixel Plant needs to run for a while to collect data.")
            print("Check back after a few days of use!\n")
            return 0

        # Generate and display report
        report = learner.export_insights_report()
        print(report)
        print()

        # Offer to save report
        save = input("Save report to file? (y/n): ").strip().lower()

        if save == 'y':
            report_file = Path(config.system.data_directory) / 'insights_report.txt'
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"\n✅ Report saved to: {report_file}")

        return 0

    except Exception as e:
        print(f"❌ Error generating insights: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

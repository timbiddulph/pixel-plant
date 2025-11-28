"""
Pattern Learning System
Learns user habits and optimal reminder timing
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)


class PatternLearner:
    """Learns and adapts to user behavior patterns"""

    def __init__(self, data_directory: str, learning_enabled: bool = True,
                 pattern_window_days: int = 7):
        """
        Initialize pattern learner

        Args:
            data_directory: Directory to store learned patterns
            learning_enabled: Enable pattern learning
            pattern_window_days: Days of history to consider
        """
        self.data_directory = Path(data_directory)
        self.learning_enabled = learning_enabled
        self.pattern_window_days = pattern_window_days

        # Ensure data directory exists
        self.data_directory.mkdir(parents=True, exist_ok=True)

        self.patterns_file = self.data_directory / 'behavior_patterns.json'

        # Pattern data
        self.activity_log = []
        self.reminder_effectiveness = defaultdict(list)
        self.typical_break_times = []
        self.hydration_patterns = []

        # Load existing patterns
        self._load_patterns()

        logger.info(f"Pattern learner initialized (learning: {learning_enabled})")

    def _load_patterns(self):
        """Load previously learned patterns"""
        if not self.patterns_file.exists():
            logger.info("No existing patterns found")
            return

        try:
            with open(self.patterns_file, 'r') as f:
                data = json.load(f)

            self.activity_log = data.get('activity_log', [])
            self.reminder_effectiveness = defaultdict(
                list,
                data.get('reminder_effectiveness', {})
            )
            self.typical_break_times = data.get('typical_break_times', [])
            self.hydration_patterns = data.get('hydration_patterns', [])

            logger.info(f"Loaded {len(self.activity_log)} activity records")

        except Exception as e:
            logger.error(f"Failed to load patterns: {e}")

    def save_patterns(self):
        """Save learned patterns to disk"""
        if not self.learning_enabled:
            return

        try:
            data = {
                'activity_log': self.activity_log[-1000:],  # Keep last 1000 records
                'reminder_effectiveness': dict(self.reminder_effectiveness),
                'typical_break_times': self.typical_break_times,
                'hydration_patterns': self.hydration_patterns,
                'last_updated': datetime.now().isoformat(),
            }

            with open(self.patterns_file, 'w') as f:
                json.dump(data, f, indent=2)

            logger.debug("Patterns saved")

        except Exception as e:
            logger.error(f"Failed to save patterns: {e}")

    def log_activity(self, activity_type: str, state: str, metadata: Optional[Dict] = None):
        """
        Log user activity

        Args:
            activity_type: Type of activity (sitting, moving, break, etc.)
            state: State or outcome
            metadata: Additional data
        """
        if not self.learning_enabled:
            return

        record = {
            'timestamp': datetime.now().isoformat(),
            'activity_type': activity_type,
            'state': state,
            'metadata': metadata or {}
        }

        self.activity_log.append(record)

        # Auto-save periodically
        if len(self.activity_log) % 50 == 0:
            self.save_patterns()

    def log_reminder_response(self, reminder_type: str, user_responded: bool,
                              response_time: Optional[float] = None):
        """
        Log how user responded to reminder

        Args:
            reminder_type: Type of reminder sent
            user_responded: True if user took action
            response_time: Time taken to respond (seconds)
        """
        if not self.learning_enabled:
            return

        effectiveness = {
            'timestamp': datetime.now().isoformat(),
            'responded': user_responded,
            'response_time': response_time,
        }

        self.reminder_effectiveness[reminder_type].append(effectiveness)

        logger.debug(f"Logged reminder response: {reminder_type} "
                    f"({'responded' if user_responded else 'ignored'})")

    def get_optimal_reminder_time(self, reminder_type: str) -> Optional[int]:
        """
        Get optimal time for a reminder based on learned patterns

        Args:
            reminder_type: Type of reminder

        Returns:
            Optimal interval in minutes, or None if no pattern learned
        """
        if not self.learning_enabled:
            return None

        # Analyze when user typically responds positively
        responses = self.reminder_effectiveness.get(reminder_type, [])

        if len(responses) < 5:  # Not enough data
            return None

        # TODO: Implement actual pattern analysis
        # For now, return default
        return None

    def get_typical_break_pattern(self) -> List[int]:
        """
        Get user's typical break times

        Returns:
            List of hour values when user typically takes breaks
        """
        # TODO: Analyze activity log for break patterns
        # Placeholder: assume breaks at 10am, 2pm, 4pm
        return [10, 14, 16]

    def should_learn_from_interaction(self) -> bool:
        """Check if we should learn from current interaction"""
        return self.learning_enabled

    def get_learning_summary(self) -> Dict:
        """
        Get summary of learned patterns

        Returns:
            Dictionary with learning statistics
        """
        return {
            'total_activities_logged': len(self.activity_log),
            'reminder_types_tracked': list(self.reminder_effectiveness.keys()),
            'learning_enabled': self.learning_enabled,
            'data_window_days': self.pattern_window_days,
        }

    def analyze_reminder_effectiveness(self, reminder_type: str) -> Dict:
        """
        Analyze how effective a reminder type has been

        Args:
            reminder_type: Type of reminder to analyze

        Returns:
            Dictionary with effectiveness metrics
        """
        responses = self.reminder_effectiveness.get(reminder_type, [])

        if len(responses) < 3:
            return {
                'sample_size': len(responses),
                'sufficient_data': False,
            }

        # Calculate metrics
        total = len(responses)
        responded = sum(1 for r in responses if r.get('responded', False))
        response_rate = responded / total if total > 0 else 0

        # Calculate average response time for those who responded
        response_times = [
            r.get('response_time', 0) for r in responses
            if r.get('responded', False) and r.get('response_time') is not None
        ]

        avg_response_time = sum(response_times) / len(response_times) if response_times else None

        return {
            'sample_size': total,
            'sufficient_data': total >= 10,
            'response_rate': response_rate,
            'responded_count': responded,
            'ignored_count': total - responded,
            'avg_response_time_seconds': avg_response_time,
            'recommendation': self._get_reminder_recommendation(response_rate),
        }

    def _get_reminder_recommendation(self, response_rate: float) -> str:
        """Get recommendation based on response rate"""
        if response_rate >= 0.7:
            return "highly_effective"
        elif response_rate >= 0.4:
            return "moderately_effective"
        elif response_rate >= 0.2:
            return "low_effectiveness"
        else:
            return "ineffective"

    def analyze_activity_patterns(self) -> Dict:
        """
        Analyze activity log for patterns

        Returns:
            Dictionary with discovered patterns
        """
        if len(self.activity_log) < 10:
            return {'sufficient_data': False}

        # Group by hour of day
        hourly_activity = defaultdict(list)

        for record in self.activity_log:
            try:
                timestamp = datetime.fromisoformat(record['timestamp'])
                hour = timestamp.hour
                hourly_activity[hour].append(record)
            except:
                continue

        # Find most active hours
        activity_counts = {
            hour: len(activities)
            for hour, activities in hourly_activity.items()
        }

        sorted_hours = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)

        most_active_hours = [hour for hour, count in sorted_hours[:3]]
        least_active_hours = [hour for hour, count in sorted_hours[-3:]]

        return {
            'sufficient_data': True,
            'total_records': len(self.activity_log),
            'most_active_hours': most_active_hours,
            'least_active_hours': least_active_hours,
            'hourly_distribution': activity_counts,
        }

    def suggest_optimal_reminder_times(self) -> List[int]:
        """
        Suggest optimal hours for reminders based on activity

        Returns:
            List of hours (0-23) when user is most receptive
        """
        patterns = self.analyze_activity_patterns()

        if not patterns.get('sufficient_data', False):
            # Default suggestions
            return [10, 14, 16]  # 10am, 2pm, 4pm

        # Suggest reminders during most active hours
        return patterns.get('most_active_hours', [10, 14, 16])

    def get_sitting_statistics(self) -> Dict:
        """
        Analyze sitting patterns

        Returns:
            Dictionary with sitting statistics
        """
        sitting_sessions = [
            record for record in self.activity_log
            if record.get('activity_type') == 'sitting' and
               record.get('state') == 'started'
        ]

        if len(sitting_sessions) < 5:
            return {'sufficient_data': False}

        # Group by day of week
        weekday_sessions = defaultdict(list)

        for session in sitting_sessions:
            try:
                timestamp = datetime.fromisoformat(session['timestamp'])
                weekday = timestamp.weekday()  # 0=Monday, 6=Sunday
                weekday_sessions[weekday].append(session)
            except:
                continue

        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']

        sessions_by_day = {
            weekday_names[day]: len(sessions)
            for day, sessions in weekday_sessions.items()
        }

        return {
            'sufficient_data': True,
            'total_sessions': len(sitting_sessions),
            'sessions_by_weekday': sessions_by_day,
            'most_sitting_day': max(sessions_by_day, key=sessions_by_day.get) if sessions_by_day else None,
        }

    def export_insights_report(self) -> str:
        """
        Generate human-readable insights report

        Returns:
            Multi-line string with insights
        """
        report = ["=" * 60]
        report.append("PIXEL PLANT - LEARNING INSIGHTS REPORT")
        report.append("=" * 60)
        report.append("")

        # Overall statistics
        summary = self.get_learning_summary()
        report.append(f"Total Activities Logged: {summary['total_activities_logged']}")
        report.append(f"Learning Enabled: {summary['learning_enabled']}")
        report.append("")

        # Reminder effectiveness
        report.append("REMINDER EFFECTIVENESS:")
        report.append("-" * 60)

        for reminder_type in summary['reminder_types_tracked']:
            analysis = self.analyze_reminder_effectiveness(reminder_type)

            if analysis['sufficient_data']:
                report.append(f"\n{reminder_type.capitalize()}:")
                report.append(f"  Response Rate: {analysis['response_rate']:.1%}")
                report.append(f"  Responded: {analysis['responded_count']}")
                report.append(f"  Ignored: {analysis['ignored_count']}")

                if analysis['avg_response_time_seconds']:
                    report.append(f"  Avg Response Time: {analysis['avg_response_time_seconds']:.1f}s")

                report.append(f"  Recommendation: {analysis['recommendation']}")
            else:
                report.append(f"\n{reminder_type.capitalize()}: Insufficient data ({analysis['sample_size']} samples)")

        report.append("")

        # Activity patterns
        report.append("ACTIVITY PATTERNS:")
        report.append("-" * 60)

        patterns = self.analyze_activity_patterns()

        if patterns.get('sufficient_data', False):
            report.append(f"\nTotal Records: {patterns['total_records']}")
            report.append(f"Most Active Hours: {', '.join(map(str, patterns['most_active_hours']))}")
            report.append(f"Least Active Hours: {', '.join(map(str, patterns['least_active_hours']))}")
        else:
            report.append("\nInsufficient data for pattern analysis")

        report.append("")

        # Sitting statistics
        report.append("SITTING PATTERNS:")
        report.append("-" * 60)

        sitting_stats = self.get_sitting_statistics()

        if sitting_stats.get('sufficient_data', False):
            report.append(f"\nTotal Sitting Sessions: {sitting_stats['total_sessions']}")

            if sitting_stats['sessions_by_weekday']:
                report.append("\nSessions by Weekday:")
                for day, count in sitting_stats['sessions_by_weekday'].items():
                    report.append(f"  {day}: {count}")

                report.append(f"\nMost Sitting: {sitting_stats['most_sitting_day']}")
        else:
            report.append("\nInsufficient data for sitting analysis")

        report.append("")

        # Recommendations
        report.append("RECOMMENDATIONS:")
        report.append("-" * 60)

        optimal_times = self.suggest_optimal_reminder_times()
        report.append(f"\nOptimal Reminder Times: {', '.join([f'{h}:00' for h in optimal_times])}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


if __name__ == '__main__':
    """Test pattern learner"""
    logging.basicConfig(level=logging.INFO)

    import tempfile
    temp_dir = tempfile.mkdtemp()

    learner = PatternLearner(data_directory=temp_dir, learning_enabled=True)

    print("=== PATTERN LEARNER TEST ===\n")

    # Log some activities
    learner.log_activity('sitting', 'started')
    learner.log_activity('break', 'taken', {'duration': 300})
    learner.log_activity('sitting', 'resumed')

    # Log reminder responses
    learner.log_reminder_response('hydration', True, 45.0)
    learner.log_reminder_response('movement', False)
    learner.log_reminder_response('hydration', True, 30.0)

    # Save patterns
    learner.save_patterns()

    # Get summary
    summary = learner.get_learning_summary()
    print("Learning Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print(f"\nPatterns saved to: {learner.patterns_file}")

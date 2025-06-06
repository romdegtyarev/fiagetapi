import argparse
import sys
import logging
from logic.session_loader import load_session
from logic.best_laps import print_best_laps, generate_best_laps_image, generate_laptime_distribution_image
from logic.results import print_results, generate_results_image, export_results_csv
from logic.position_changes import generate_position_changes_image
from logic.strategy import generate_strategy_image
from logic.driver_styling import generate_driver_styling_image


def main() -> None:
    """
    CLI interface for analyzing F1 sessions using FastF1.
    """
    logging.getLogger("fastf1").setLevel(logging.ERROR)
    logging.getLogger("fastf1.req").setLevel(logging.ERROR)
    logging.getLogger("fastf1.core").setLevel(logging.ERROR)
    parser = argparse.ArgumentParser(description="CLI for analyzing F1 sessions via FastF1")
    parser.add_argument("--year", type=int, required=True, help="Season year, e.g., 2024")
    parser.add_argument("--gp", type=str, required=True, help="Grand Prix name, e.g., Monaco")
    parser.add_argument("--type", type=str, required=True, choices=["FP1", "FP2", "FP3", "Q", "R", "SQ", "S"], help="Session type: FP1, FP2, FP3, Q, R, S")

    parser.add_argument("--best-laps", action="store_true", help="Display best laps and save image")
    parser.add_argument("--results", action="store_true", help="Display results and save image")
    parser.add_argument("--position-changes", action="store_true", help="Display position changes graph")
    parser.add_argument("--strategy", action="store_true", help="Display tire strategy graph")
    parser.add_argument("--driver-styling", action="store_true", help="Display driver lap performance by compound")
    parser.add_argument("--driver", type=str, help="Driver abbreviation, e.g., LEC")

    args = parser.parse_args()

    try:
        session = load_session(args.year, args.gp, args.type.upper())
    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        sys.exit(1)

    if args.best_laps:
        try:
            print_best_laps(session)
            path = generate_best_laps_image(session)
            print(f"📈 Best laps chart saved to: {path}")
            path = generate_laptime_distribution_image(session)
            print(f"📈 Laptime distribution saved to: {path}")
        except Exception as e:
            print(f"❌ Error generating best laps chart: {e}")
            sys.exit(1)

    if args.results:
        try:
            print_results(session)
            path = generate_results_image(session)
            print(f"📈 Session results saved to: {path}")
            path = export_results_csv(session)
            print(f"📈 Session results saved to: {path}")
        except Exception as e:
            print(f"❌ Error processing session results: {e}")
            sys.exit(1)

    if args.position_changes:
        try:
            path = generate_position_changes_image(session)
            print(f"📈 Position changes graph saved to: {path}")
        except Exception as e:
            print(f"❌ Error generating position changes graph: {e}")
            sys.exit(1)

    if args.strategy:
        try:
            path = generate_strategy_image(session)
            print(f"📈 Tire strategy graph saved to: {path}")
        except Exception as e:
            print(f"❌ Error generating tire strategy graph: {e}")
            sys.exit(1)

    if args.driver_styling:
        if not args.driver:
            print("❌ Error: --driver-styling requires --driver to be specified (e.g., --driver LEC)")
            sys.exit(1)
        try:
            path = generate_driver_styling_image(session, args.driver.upper())
            print(f"📈 Driver lap styling graph saved to: {path}")
        except Exception as e:
            print(f"❌ Error generating driver styling image: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

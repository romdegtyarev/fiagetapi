import argparse
from logic.session_loader import load_session
from logic.best_laps import print_best_laps, generate_best_laps_image
from logic.summary import print_summary
from logic.results import print_results, generate_results_image


def main():
    """
    CLI interface for analyzing F1 sessions using FastF1.
    """
    parser = argparse.ArgumentParser(description="CLI for analyzing F1 sessions via FastF1")
    parser.add_argument("--year", type=int, required=True, help="Season year, e.g., 2024")
    parser.add_argument("--gp", type=str, required=True, help="Grand Prix name, e.g., Monaco")
    parser.add_argument("--type", type=str, required=True,
                        choices=["FP1", "FP2", "FP3", "Q", "R", "S"],
                        help="Session type: FP1, FP2, FP3, Q, R, S")
    parser.add_argument("--best-laps", action="store_true", help="Display best laps and save image")
    parser.add_argument("--results", action="store_true", help="Display results and save image")
    parser.add_argument("--summary", action="store_true", help="Display session summary")

    args = parser.parse_args(

    try:
        session = load_session(args.year, args.gp, args.type.upper())
    except Exception as e:
        print(f"❌ Failed to load session: {e}")
        return

    if args.best_laps:
        try:
            print_best_laps(session)
            path = generate_best_laps_image(session)
            print(f"📈 Best laps chart saved to: {path}")
        except Exception as e:
            print(f"❌ Error generating best laps chart: {e}")

    if args.summary:
        try:
            print_summary(session)
        except Exception as e:
            print(f"❌ Error displaying summary: {e}")

    if args.results:
        try:
            print_results(session)
            path = generate_results_image(session)
            print(f"📈 Session results saved to: {path}")
        except Exception as e:
            print(f"❌ Error processing session results: {e}")

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

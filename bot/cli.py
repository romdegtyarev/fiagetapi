from logic.session_loader import load_session
from logic.best_laps import print_best_laps
from logic.best_laps import generate_best_laps_image
from logic.summary import print_summary
from logic.results import generate_results_image
import argparse


def main():
    parser = argparse.ArgumentParser(description="CLI для анализа F1 сессий через FastF1")
    parser.add_argument("--year", type=int, required=True, help="Год сезона, например 2024")
    parser.add_argument("--gp", type=str, required=True, help="Название этапа, например Monaco")
    parser.add_argument("--type", type=str, required=True, help="Тип сессии: FP1, FP2, FP3, Q, R, S")

    parser.add_argument("--best-laps", action="store_true", help="Показать лучшие круги")
    parser.add_argument("--summary", action="store_true", help="Краткий анализ")
    parser.add_argument("--results", action="store_true", help="Показать результаты и сохранить изображение")

    args = parser.parse_args()

    session = load_session(args.year, args.gp, args.type.upper())

    if args.best_laps:
        print_best_laps(session)
        path = generate_best_laps_image(session)
        print(f"📈 График лучших кругов сохранён в: {path}")

    if args.summary:
        print_summary(session)

    if args.results:
        path = generate_results_image(session)
        print(f"📈 Результаты сохранены в: {path}")


if __name__ == "__main__":
    main()

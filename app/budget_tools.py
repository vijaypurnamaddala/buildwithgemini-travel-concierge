def calculate_trip_budget(
    num_days: int,
    lodging_per_night: float = 0.0,
    food_per_day: float = 0.0,
    activities_total: float = 0.0,
    transport_total: float = 0.0,
) -> dict:
    """Calculates a detailed trip budget breakdown and total estimated cost.

    Args:
        num_days: Total number of days for the trip.
        lodging_per_night: Estimated lodging or hotel cost per night.
        food_per_day: Estimated food and dining expense per day.
        activities_total: Total estimated cost for tours, entrance fees, and activities.
        transport_total: Total estimated cost for flights, trains, or local transit.

    Returns:
        A dictionary containing cost breakdown per category, grand total, and daily average.
    """
    total_lodging = num_days * lodging_per_night
    total_food = num_days * food_per_day
    grand_total = total_lodging + total_food + activities_total + transport_total
    daily_average = grand_total / num_days if num_days > 0 else 0.0

    return {
        "num_days": num_days,
        "lodging_total": round(total_lodging, 2),
        "food_total": round(total_food, 2),
        "activities_total": round(activities_total, 2),
        "transport_total": round(transport_total, 2),
        "grand_total": round(grand_total, 2),
        "daily_average": round(daily_average, 2),
    }

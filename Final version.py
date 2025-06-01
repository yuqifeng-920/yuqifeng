import heapq
import pandas as pd
import math


def allocate_seats_dhondt(votes, total_seats):
    divisors = range(1, total_seats + 1)
    quotients = []

    for party, vote_count in votes.items():
        for divisor in divisors:
            heapq.heappush(quotients, (-vote_count / divisor, party))

    seat_allocations = {party: 0 for party in votes}

    for _ in range(total_seats):
        _, party = heapq.heappop(quotients)
        seat_allocations[party] += 1

    return seat_allocations


def allocate_seats_saint_lague(votes, total_seats):
    divisors = [1] + list(range(3, total_seats * 2, 2))
    quotients = []

    for party, vote_count in votes.items():
        for divisor in divisors:
            heapq.heappush(quotients, (-vote_count / divisor, party))

    seat_allocations = {party: 0 for party in votes}

    for _ in range(total_seats):
        _, party = heapq.heappop(quotients)
        seat_allocations[party] += 1

    return seat_allocations


def allocate_seats_modified_saint_lague(votes, total_seats):
    divisors = [1.4, 3] + list(range(5, total_seats * 2, 2))
    quotients = []

    for party, vote_count in votes.items():
        for divisor in divisors:
            heapq.heappush(quotients, (-vote_count / divisor, party))

    seat_allocations = {party: 0 for party in votes}

    for _ in range(total_seats):
        _, party = heapq.heappop(quotients)
        seat_allocations[party] += 1

    return seat_allocations


def allocate_seats_hare(votes, total_seats):
    quota = sum(votes.values()) / total_seats
    return allocate_seats_with_quota(votes, total_seats, quota)


def allocate_seats_with_quota(votes, total_seats, quota):
    if total_seats == 0:
        return {party: 0 for party in votes}

    seat_allocations = {party: math.floor(votes[party] / quota) for party in votes}
    allocated_seats = sum(seat_allocations.values())

    remaining_seats = total_seats - allocated_seats
    remainders = {party: (votes[party] / quota) - seat_allocations[party] for party in votes}
    sorted_parties = sorted(remainders.keys(), key=lambda p: remainders[p], reverse=True)

    for i in range(remaining_seats):
        seat_allocations[sorted_parties[i]] += 1

    return seat_allocations


def allocate_seats_droop(votes, total_seats):
    quota = (sum(votes.values()) / (total_seats + 1)) + 1
    return allocate_seats_with_quota(votes, total_seats, quota)


def allocate_seats_hagenbach_bischoff(votes, total_seats):
    quota = sum(votes.values()) / (total_seats + 1)
    return allocate_seats_with_quota(votes, total_seats, quota)


def analyze_country(df, country):
    df_filtered = df[df['Country'] == country]

    if df_filtered.empty:
        print(f"Error: No data found for {country}. Please check the election results file.")
        return

    total_votes = {party: df_filtered[df_filtered['Party'] == party]['Votes'].sum() for party in
                   df_filtered['Party'].unique()}
    total_seats = df_filtered['Seats'].sum()

    if total_seats == 0:
        print(f"Error: No seats found for {country}. Please check the seat allocation file.")
        return

    results = {
        "D'Hondt": allocate_seats_dhondt(total_votes, total_seats),
        "Saint-Lague": allocate_seats_saint_lague(total_votes, total_seats),
        "Modified Saint-Lague": allocate_seats_modified_saint_lague(total_votes, total_seats),
        "Hare": allocate_seats_hare(total_votes, total_seats),
        "Droop": allocate_seats_droop(total_votes, total_seats),
        "Hagenbach-Bischoff": allocate_seats_hagenbach_bischoff(total_votes, total_seats)
    }

    print("\nFinal Results for", country, "(Copy-Paste to Excel):")
    print(
        "Party\tVote Share (%)\tD'Hondt Seats\tD'Hondt Share (%)\tSaint-Lague Seats\tSaint-Lague Share (%)\tModified Saint-Lague Seats\tModified Saint-Lague Share (%)\tHare Seats\tHare Share (%)\tDroop Seats\tDroop Share (%)\tHagenbach-Bischoff Seats\tHagenbach-Bischoff Share (%)")

    total_vote_count = sum(total_votes.values())
    sorted_parties = sorted(total_votes.keys(), key=lambda p: total_votes[p], reverse=True)

    for party in sorted_parties:
        vote_share = (total_votes[party] / total_vote_count) * 100 if total_vote_count > 0 else 0
        seat_shares = []
        for method in results:
            seats = results[method].get(party, 0)
            seat_share = (seats / total_seats) * 100 if total_seats > 0 else 0
            seat_shares.append(f"{seats}\t{seat_share:.2f}")
        print(f"{party}\t{vote_share:.2f}\t" + "\t".join(seat_shares))


def main():
    file_path = input("Enter the path to the election results Excel file: ")
    df = pd.read_excel(file_path)

    if 'Country' not in df.columns or 'Party' not in df.columns or 'Votes' not in df.columns or 'Seats' not in df.columns:
        print("Error: Excel file must contain 'Country', 'Party', 'Votes', and 'Seats' columns.")
        return

    while True:
        country = input("Enter the country you want to analyze (or type 'exit' to stop): ")
        if country.lower() == 'exit':
            break
        analyze_country(df, country)


if __name__ == "__main__":
    main()

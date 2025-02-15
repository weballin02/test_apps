import streamlit as st
import requests

def fetch_odds(api_key, sport_key, region='us', markets='spreads,totals'):
    """
    Fetches sports betting odds from The Odds API, limited to Bovada.

    Args:
        api_key (str): Your API key for The Odds API.
        sport_key (str): The sport key (e.g., 'basketball_ncaab').
        region (str): The region for bookmakers ('us', 'uk', 'eu', 'au').
        markets (str): Comma-separated betting markets ('h2h', 'spreads', 'totals').

    Returns:
        list: A list of events with betting odds from Bovada.
    """
    url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds'
    params = {
        'apiKey': api_key,
        'regions': region,
        'markets': markets,
        'bookmakers': 'bovada',  # Ensures only Bovada odds are fetched
        'oddsFormat': 'american',
        'dateFormat': 'iso'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return []
    return response.json()

def main():
    st.title("Sports Betting Odds Viewer (Bovada Only)")

    api_key = st.text_input("Enter your The Odds API key:", type="password")
    if not api_key:
        st.warning("Please enter your API key to continue.")
        st.stop()

    sports = {
        'NFL': 'americanfootball_nfl',
        'NBA': 'basketball_nba',
        'MLB': 'baseball_mlb',
        'NHL': 'icehockey_nhl',
        'EPL': 'soccer_epl',
        'NCAAB': 'basketball_ncaab'  # NCAAB Added
    }
    sport = st.selectbox("Choose a sport:", list(sports.keys()))
    region = st.selectbox("Choose a region:", ['us', 'uk', 'eu', 'au'])

    if st.button("Fetch Odds"):
        with st.spinner("Fetching odds..."):
            odds_data = fetch_odds(api_key, sports[sport], region)
            if odds_data:
                for event in odds_data:
                    st.subheader(f"{event['home_team']} vs {event['away_team']}")
                    st.write(f"Commence Time: {event['commence_time']}")
                    for bookmaker in event['bookmakers']:
                        if bookmaker['key'] == 'bovada':  # Ensures only Bovada is displayed
                            st.write(f"**Bookmaker:** {bookmaker['title']}")
                            for market in bookmaker['markets']:
                                st.write(f"**Market:** {market['key']}")
                                for outcome in market['outcomes']:
                                    st.write(f"{outcome['name']}: {outcome['price']}")
                    st.write("---")
            else:
                st.info("No odds data available for the selected options.")

if __name__ == "__main__":
    main()

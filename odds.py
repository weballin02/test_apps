import streamlit as st
import requests

def fetch_odds(api_key, sport_key, market, region='us'):
    """
    Fetch sports betting odds from The Odds API, limiting the response to Bovada and
    requesting only the selected market(s).

    Args:
        api_key (str): Your API key for The Odds API.
        sport_key (str): The sport key (e.g., 'basketball_ncaab').
        market (str): The market to request (e.g., 'spreads', 'totals', or 'spreads,totals').
        region (str): The region for bookmakers. Bovada is available only in 'us'.

    Returns:
        list: A list of events (dictionaries) returned by the API.
    """
    url = f'https://api.the-odds-api.com/v4/sports/{sport_key}/odds'
    params = {
        'apiKey': api_key,
        'regions': region,         # For Bovada, the region must be 'us'
        'markets': market,         # Request the selected market(s)
        'bookmakers': 'bovada',     # Limit to Bovada only
        'oddsFormat': 'american',
        'dateFormat': 'iso'
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        st.error(f"Error fetching data: {response.status_code} - {response.text}")
        return []
    return response.json()

def main():
    st.title("Sports Betting Odds Viewer (Bovada: Selected Market Only)")

    # Prompt for API key
    api_key = st.text_input("Enter your The Odds API key:", type="password")
    if not api_key:
        st.warning("Please enter your API key to continue.")
        st.stop()

    # Define available sports
    sports = {
        'NFL': 'americanfootball_nfl',
        'NBA': 'basketball_nba',
        'MLB': 'baseball_mlb',
        'NHL': 'icehockey_nhl',
        'EPL': 'soccer_epl',
        'NCAAB': 'basketball_ncaab'
    }
    sport = st.selectbox("Choose a sport:", list(sports.keys()))

    # Although a region select box is provided, Bovada is US-only.
    region = st.selectbox("Choose a region (Bovada is available only in the US):", ['us', 'uk', 'eu', 'au'])
    if region != 'us':
        st.warning("Bovada is available only in the US region. Overriding selection to 'us'.")
        region = 'us'

    # Allow user to select a market type
    selected_market = st.selectbox("Choose a market:", ["spreads", "totals", "spreads,totals"])

    if st.button("Fetch Odds"):
        with st.spinner("Fetching odds..."):
            events = fetch_odds(api_key, sports[sport], selected_market, region)
            if not events:
                st.info("No odds data available for the selected options.")
                return

            # Process each event, filtering for Bovada data
            for event in events:
                # Filter bookmakers to only include Bovada (API should return only Bovada, but we double-check)
                bovada_data = [bm for bm in event.get('bookmakers', []) if bm.get('key') == 'bovada']
                if not bovada_data:
                    continue  # Skip event if Bovada data is not available

                st.subheader(f"{event.get('home_team')} vs {event.get('away_team')}")
                st.write(f"Commence Time: {event.get('commence_time')}")
                
                for bm in bovada_data:
                    st.write(f"**Bookmaker:** {bm.get('title', 'Unknown')}")
                    
                    # Determine which markets to display based on the selection
                    market_keys = [m.strip() for m in selected_market.split(',')]
                    markets = [m for m in bm.get('markets', []) if m.get('key') in market_keys]
                    if not markets:
                        st.write("No selected market data available for this event.")
                    else:
                        for market in markets:
                            st.write(f"**Market:** {market.get('key')}")
                            for outcome in market.get('outcomes', []):
                                point_info = f" (Point: {outcome.get('point')})" if outcome.get('point') is not None else ""
                                st.write(f"{outcome.get('name')}: {outcome.get('price')}{point_info}")
                st.write("---")

if __name__ == "__main__":
    main()

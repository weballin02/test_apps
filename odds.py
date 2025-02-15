import streamlit as st
import requests

def fetch_odds(api_key, sport_key, bookmaker, odds_format):
    """
    Fetches odds from The Odds API for a specified sport using only the spreads and totals markets,
    restricted to one bookmaker and a fixed region ("us").
    
    Parameters:
        api_key (str): Your Odds API key.
        sport_key (str): The API sport key (e.g., "americanfootball_nfl").
        bookmaker (str): The bookmaker key (e.g., "fanduel").
        odds_format (str): Desired odds format ('decimal' or 'american').
    
    Returns:
        dict or None: JSON response from the API if successful; otherwise, None.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    params = {
        "apiKey": api_key,
        "regions": "us",              # Required region parameter
        "bookmakers": bookmaker,       # Restrict results to one bookmaker
        "markets": "spreads,totals",   # Fixed markets
        "oddsFormat": odds_format.lower()
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch odds. Error Code: {response.status_code}")
        return None

# Mapping from display names to API sport keys
sport_mapping = {
    "American Football - NFL": "americanfootball_nfl",
    "American Football - NCAAF": "americanfootball_ncaaf",
    "Basketball - NBA": "basketball_nba",
    "Baseball - MLB": "baseball_mlb"
}

# Streamlit UI Layout
st.title("Sports Odds Fetcher")

# Input for API key
api_key = st.text_input("Enter your Odds API Key", type="password")

# Sport selection using proper mapping
selected_sport_display = st.selectbox("Select League/Competition", list(sport_mapping.keys()))
selected_sport_key = sport_mapping[selected_sport_display]

# Single bookmaker selection dropdown
bookmakers = [
    ("FanDuel", "fanduel"),
    ("DraftKings", "draftkings"),
    ("BetMGM", "betmgm"),
    ("Caesars", "caesars"),
    ("William Hill (US)", "williamhill_us")
]
selected_bookmaker_label = st.selectbox("Select Bookmaker", [b[0] for b in bookmakers])
selected_bookmaker = dict(bookmakers)[selected_bookmaker_label]

# Odds format selection
odds_format = st.radio("Select Odds Format", ["Decimal", "American"])

# Optional output tab name
output_tab = st.text_input("Output Tab Name (Optional)", "Odds Data")

# Display fixed usage cost info: 2 markets x 1 region = 2
st.write("Max. Usage Cost: 2 (2 markets x 1 region)")

# Fetch odds action
if st.button("Fetch"):
    if not api_key:
        st.error("Please enter your API key.")
    else:
        data = fetch_odds(api_key, selected_sport_key, selected_bookmaker, odds_format)
        if data:
            st.success("Odds Data Fetched Successfully!")
            st.write(data)

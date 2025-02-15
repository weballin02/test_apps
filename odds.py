import streamlit as st
import requests

def fetch_odds(api_key, sport, bookmaker, odds_format):
    """
    Fetches the odds for a given sport from the Odds API for only the spreads
    and totals markets and for a single bookmaker.

    Parameters:
        api_key (str): Your Odds API key.
        sport (str): The selected sport (e.g., "American Football - NFL").
        bookmaker (str): The bookmaker key to restrict the results (e.g., "fanduel").
        odds_format (str): Desired odds format ('decimal' or 'american').

    Returns:
        dict or None: JSON response from the API if successful, otherwise None.
    """
    # Convert sport name to API sport key format (lowercase and underscores)
    sport_key = sport.lower().replace(" ", "_").replace("-", "_")
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds/"
    
    # Set parameters: restrict to one bookmaker and fixed markets ("spreads" and "totals")
    params = {
        "apiKey": api_key,
        "bookmakers": bookmaker,
        "markets": "spreads,totals",
        "oddsFormat": odds_format.lower()
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch odds. Error Code: {response.status_code}")
        return None

# Streamlit UI Layout
st.title("Sports Odds Fetcher")

# API key input
api_key = st.text_input("Enter your Odds API Key", type="password")

# Sport selection dropdown
sports = [
    "American Football - NFL",
    "American Football - NCAAF",
    "Basketball - NBA",
    "Baseball - MLB"
]
selected_sport = st.selectbox("Select League/Competition", sports)

# Bookmaker selection dropdown (single bookmaker)
bookmakers = [
    ("FanDuel", "fanduel"),
    ("DraftKings", "draftkings"),
    ("BetMGM", "betmgm"),
    ("Caesars", "caesars"),
    ("William Hill (US)", "williamhill_us")
]
selected_bookmaker_label = st.selectbox("Select Bookmaker", [b[0] for b in bookmakers])
# Get the bookmaker key from the selected label
selected_bookmaker_key = dict(bookmakers)[selected_bookmaker_label]

# Odds format radio button
odds_format = st.radio("Select Odds Format", ["Decimal", "American"])

# Optional output tab name
output_tab = st.text_input("Output Tab Name (Optional)", "Odds Data")

# Display fixed cost: 2 markets x 1 bookmaker
st.write("Max. Usage Cost: 2 (2 markets x 1 bookmaker)")

# Fetch button and action
if st.button("Fetch"):
    if not api_key:
        st.error("Please enter your API key.")
    else:
        data = fetch_odds(api_key, selected_sport, selected_bookmaker_key, odds_format)
        if data:
            st.success("Odds Data Fetched Successfully!")
            st.write(data)

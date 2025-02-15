# Prompt user for API key
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

# Although region selection is available, Bovada is only available in the US.
region = st.selectbox("Choose a region (Bovada is available only in the US):", ['us', 'uk', 'eu', 'au'])
if region != 'us':
    st.warning("Bovada is available only in the US region. Overriding selection to 'us'.")
    region = 'us'

# Fetch odds when the user clicks the button
if st.button("Fetch Odds"):
    with st.spinner("Fetching odds..."):
        odds_data = fetch_odds(api_key, sports[sport], region)
        if odds_data:
            for event in odds_data:
                st.subheader(f"{event['home_team']} vs {event['away_team']}")
                st.write(f"Commence Time: {event['commence_time']}")
                
                # Loop over bookmakers in the event; display Bovada data only
                for bookmaker in event.get('bookmakers', []):
                    if bookmaker.get('key') == 'bovada':
                        st.write(f"**Bookmaker:** {bookmaker.get('title', 'Unknown')}")
                        # Loop over markets (spread and totals)
                        for market in bookmaker.get('markets', []):
                            st.write(f"**Market:** {market.get('key')}")
                            for outcome in market.get('outcomes', []):
                                point_info = ""
                                # Add point information if available
                                if outcome.get('point') is not None:
                                    point_info = f" (Point: {outcome.get('point')})"
                                st.write(f"{outcome.get('name')}: {outcome.get('price')}{point_info}")
                st.write("---")
        else:
            st.info("No odds data available for the selected options.")

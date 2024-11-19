import streamlit as st
from datetime import datetime

# Initialize session state for data persistence
if 'priorities' not in st.session_state:
    st.session_state.priorities = [{"text": "", "done": False} for _ in range(3)]
if 'notes' not in st.session_state:
    st.session_state.notes = ""
if 'schedule' not in st.session_state:
    st.session_state.schedule = ["" for _ in range(36)]  # 18 hours * 2 slots per hour

def save_data():
    date = st.session_state.date
    data = {
        'priorities': [
            {
                "text": st.session_state[f"priority_text_{i}"],
                "done": st.session_state[f"priority_done_{i}"]
            } for i in range(3)
        ],
        'notes': st.session_state.notes,
        'schedule': [st.session_state[f"slot_{i}_{slot}"] 
                     for i in range(18) for slot in ['00', '30']]
    }
    st.session_state[f'data_{date}'] = data
    st.success("Data saved successfully!")

def load_data():
    date = st.session_state.date
    if f'data_{date}' in st.session_state:
        data = st.session_state[f'data_{date}']
        
        # Update priorities
        for i in range(3):
            st.session_state[f"priority_text_{i}"] = data['priorities'][i]["text"]
            st.session_state[f"priority_done_{i}"] = data['priorities'][i]["done"]
        
        # Update notes
        st.session_state.notes = data['notes']
        
        # Update schedule
        for i in range(18):
            for slot in ['00', '30']:
                idx = i * 2 + (0 if slot == '00' else 1)
                st.session_state[f"slot_{i}_{slot}"] = data['schedule'][idx]
    else:
        # Clear all fields
        for i in range(3):
            st.session_state[f"priority_text_{i}"] = ""
            st.session_state[f"priority_done_{i}"] = False
        st.session_state.notes = ""
        for i in range(18):
            for slot in ['00', '30']:
                st.session_state[f"slot_{i}_{slot}"] = ""

# Page configuration
st.set_page_config(page_title="Responsive Timebox Planner", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .time-slot {
        width: 100%;
        height: 40px;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 5px;
        margin: 5px 0;
        font-size: 1rem;
    }
    .current-slot {
        width: 100%;
        height: 40px;
        border: 2px solid #007aff;
        border-radius: 8px;
        padding: 5px;
        margin: 5px 0;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Create two columns for layout
col1, col2 = st.columns([1, 2])

# Left Column - Priorities and Notes
with col1:
    st.subheader("Priorities")
    
    # Priority items
    for i in range(3):
        cols = st.columns([1, 6])
        with cols[0]:
            st.checkbox("", key=f"priority_done_{i}")
        with cols[1]:
            st.text_input("", key=f"priority_text_{i}",
                          placeholder=f"Priority {i+1}")
    
    st.subheader("Notes")
    st.text_area("", key="notes", height=400,
                 placeholder="Add your notes here...")

# Right Column - Date and Schedule
with col2:
    # Date picker
    st.date_input("Date:", value=datetime.now(),
                  key="date", on_change=load_data)
    
    # Schedule
    hours = ["5", "6", "7", "8", "9", "10", "11", "12", 
             "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    
    # Get current time for highlighting
    current_time = datetime.now()
    current_hour = current_time.hour
    current_minute = current_time.minute
    
    # Adjust 24-hour clock to match 12-hour display
    current_hour_12 = current_hour % 12 or 12
    
    # Determine if the current slot is :00 or :30
    is_30_min = current_minute >= 30
    
    # Create schedule grid
    for i, hour in enumerate(hours):
        cols = st.columns([1, 2, 2])
        
        with cols[0]:
            st.markdown(f"### {hour}")
        
        # :00 slot
        with cols[1]:
            is_current_00 = (int(hour) == current_hour_12 and not is_30_min)
            css_class = "current-slot" if is_current_00 else "time-slot"
            st.markdown(
                f'<input class="{css_class}" type="text" placeholder="{hour}:00" value="{st.session_state.get(f"slot_{i}_00", "")}" />',
                unsafe_allow_html=True
            )
        
        # :30 slot
        with cols[2]:
            is_current_30 = (int(hour) == current_hour_12 and is_30_min)
            css_class = "current-slot" if is_current_30 else "time-slot"
            st.markdown(
                f'<input class="{css_class}" type="text" placeholder="{hour}:30" value="{st.session_state.get(f"slot_{i}_30", "")}" />',
                unsafe_allow_html=True
            )

    # Save button
    if st.button("Save", type="primary"):
        save_data()

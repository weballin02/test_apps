import streamlit as st
from datetime import datetime
import random
import json

# Initialize session state
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'show_premium' not in st.session_state:
    st.session_state.show_premium = False

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .success-tip {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f8ff;
        margin: 1rem 0;
    }
    .premium-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #fff3e0;
        margin: 1rem 0;
        border: 2px solid #ffd700;
    }
</style>
""", unsafe_allow_html=True)

def get_success_tips(goal_type):
    tips = {
        "Make More Money 💰": [
            "Start tracking all expenses daily",
            "Research high-income skills in your field",
            "Create multiple income streams",
            "Network with successful people",
            "Learn about passive income",
        ],
        "Find Love ❤️": [
            "Work on self-improvement daily",
            "Expand your social circle",
            "Try new hobbies to meet people",
            "Practice active listening",
            "Build confidence through achievements",
        ],
        "Get Fit 💪": [
            "Start with small daily exercises",
            "Plan your meals ahead",
            "Track your progress weekly",
            "Find a workout buddy",
            "Set specific fitness goals",
        ],
        "Career Growth 📈": [
            "Update your skills regularly",
            "Build your professional network",
            "Seek mentorship opportunities",
            "Document your achievements",
            "Create a 5-year plan",
        ],
        "Start Business 🚀": [
            "Research market needs",
            "Start with minimal investment",
            "Build an online presence",
            "Network with other entrepreneurs",
            "Learn basic accounting",
        ]
    }
    return tips.get(goal_type, ["Set clear goals", "Take action daily"])

def main():
    st.title("🎯 Success AI Coach")
    st.markdown("### Your Personal AI Success Assistant")
    
    with st.container():
        col1, col2 = st.columns([2,1])
        
        with col1:
            goal_type = st.selectbox(
                "What's Your #1 Goal?",
                ["Make More Money 💰", "Find Love ❤️", "Get Fit 💪", 
                 "Career Growth 📈", "Start Business 🚀"]
            )
            
            motivation_level = st.slider(
                "How motivated are you to achieve this goal? (1-10)",
                1, 10, 7
            )
            
            timeframe = st.select_slider(
                "When do you want to achieve this?",
                options=["1 month", "3 months", "6 months", "1 year"]
            )

        with col2:
            st.markdown("### Why Use Success AI?")
            st.markdown("""
            ✨ Personalized guidance
            🎯 Clear action steps
            📈 Progress tracking
            🤖 AI-powered insights
            """)

    if st.button("Generate My Success Plan 🚀"):
        st.session_state.show_premium = True
        
        # Show immediate value
        st.success(f"🎯 Goal Analysis Complete!")
        
        # Success probability based on motivation
        probability = min(motivation_level * 10, 95)
        st.markdown(f"### Your Success Probability: {probability}%")
        
        # Get relevant tips
        tips = get_success_tips(goal_type)
        
        # Show one free tip
        st.markdown("### Your First Action Step:")
        st.markdown(f"```{tips[0]}```")
        
        # Premium teaser
        st.markdown("""
        <div class="premium-box">
            <h3>🌟 Unlock Your Full Success Plan</h3>
            <p>Premium members get:</p>
            <ul>
                <li>✓ Complete 30-day action plan</li>
                <li>✓ Daily success tasks</li>
                <li>✓ Progress tracking dashboard</li>
                <li>✓ AI-powered recommendations</li>
                <li>✓ Success community access</li>
            </ul>
            <p><strong>Special Launch Price: $4.99/month</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add payment button (integrate with your payment processor)
        st.button("🔓 Upgrade to Premium Now")
        
        # Free value to encourage sharing
        st.markdown("### Quick Success Tips")
        for tip in tips[1:3]:  # Show 2 more tips
            st.markdown(f"• {tip}")
            
        # Social proof
        st.markdown("""
        ### What Others Are Saying
        > "This app helped me stay focused and achieve my goals!" - Sarah K.
        
        > "The daily tasks make success manageable" - John M.
        """)

if __name__ == "__main__":
    main()
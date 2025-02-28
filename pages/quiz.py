import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Gen Z Slang Quiz", page_icon="💬", layout="centered")

# Add title and description
st.title("Gen Z Slang Quiz 💬")
st.write("Test your knowledge of Gen Z slang terms!")

@st.cache_data
def load_data():
    # Create sample data
    sample_data = {
        'keyword': ['no cap', 'slay', 'rizz', 'sus', 'bussin', 'mid', 'W', 'L', 'based', 'yeet'],
        'description': [
            'Not lying or exaggerating',
            'To do something with confidence or style',
            'Charisma or charm, especially in romantic situations',
            'Suspicious or questionable',
            'Really good, especially for food',
            'Average or mediocre',
            'Win or success',
            'Loss or failure',
            'Being yourself without caring about others\' opinions',
            'To throw something with force'
        ]
    }
    return pd.DataFrame(sample_data)

# Initialize session state variables if they don't exist
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'options' not in st.session_state:
    st.session_state.options = None
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = None
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = None
if 'feedback_shown' not in st.session_state:
    st.session_state.feedback_shown = False
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = []
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0

# Function to start the quiz
def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.quiz_completed = False
    st.session_state.score = 0
    st.session_state.question_number = 0
    st.session_state.feedback_shown = False
    st.session_state.quiz_results = []
    load_next_question()

# Function to load the next question
def load_next_question():
    if st.session_state.question_number < st.session_state.num_questions:
        # Get a random row from the dataframe
        row = st.session_state.df.sample(n=1).iloc[0]
        correct_answer = row['description']
        
        # Get wrong answers - make sure we have enough options
        available_wrong = st.session_state.df[st.session_state.df['description'] != correct_answer]
        num_wrong = min(3, len(available_wrong))
        
        wrong_answers = available_wrong.sample(n=num_wrong)['description'].tolist()
        options = [correct_answer] + wrong_answers
        random.shuffle(options)
        
        # Store the current question info in session state
        st.session_state.current_question = row['keyword']
        st.session_state.options = options
        st.session_state.correct_answer = correct_answer
        st.session_state.user_answer = None
        st.session_state.feedback_shown = False
    else:
        st.session_state.quiz_completed = True
        # Update high score if current score is higher
        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

# Function to handle the answer submission
def submit_answer(selected_option):
    if st.session_state.question_number >= st.session_state.num_questions:
        return
    
    st.session_state.user_answer = selected_option
    st.session_state.feedback_shown = True
    
    # Track results for each question
    is_correct = selected_option == st.session_state.correct_answer
    if is_correct:
        st.session_state.score += 1
    
    # Save the question result
    st.session_state.quiz_results.append({
        'question': st.session_state.current_question,
        'user_answer': selected_option,
        'correct_answer': st.session_state.correct_answer,
        'is_correct': is_correct
    })
    
    # Increment the question number only if there are still questions left
    if st.session_state.question_number + 1 < st.session_state.num_questions:
        st.session_state.question_number += 1
    else:
        st.session_state.quiz_completed = True

# Function to handle the next question button
def next_question():
    if st.session_state.question_number < st.session_state.num_questions:
        load_next_question()

# Create a pie chart for the score
def create_score_chart(score, total):
    fig, ax = plt.subplots(figsize=(4, 4))
    labels = ['Correct', 'Incorrect']
    sizes = [score, total - score]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)
    
    ax.pie(sizes, explode=explode, labels=labels, colors=colors,
           autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')
    return fig

# Load the data
df = load_data()
st.session_state.df = df

# Quiz settings
col1, col2 = st.columns(2)
with col1:
    num_questions = st.number_input("Number of questions", min_value=1, max_value=len(df), value=5, step=1)
with col2:
    st.session_state.num_questions = num_questions
    start_button = st.button("Start Quiz", on_click=start_quiz)

# Quiz display
if st.session_state.quiz_started and not st.session_state.quiz_completed:
    progress = st.progress(st.session_state.question_number / st.session_state.num_questions)
    st.write(f"Question {st.session_state.question_number + 1} of {st.session_state.num_questions}")
    st.subheader(f"What does '{st.session_state.current_question}' mean?")
    
    if not st.session_state.feedback_shown:
        option = st.radio("Select your answer:", st.session_state.options, key=f"q_{st.session_state.question_number}")
        st.button("Submit Answer", on_click=submit_answer, args=(option,))
    else:
        if st.session_state.user_answer == st.session_state.correct_answer:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! The correct answer is: {st.session_state.correct_answer}")
        st.button("Next Question", on_click=next_question)

if st.session_state.quiz_completed:
    st.balloons()
    percentage = (st.session_state.score / st.session_state.num_questions) * 100
    st.markdown(f"<h1 style='text-align: center;'>Your Score: {st.session_state.score}/{st.session_state.num_questions}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{percentage:.1f}%</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>High Score: {st.session_state.high_score}/{st.session_state.num_questions}</h3>", unsafe_allow_html=True)

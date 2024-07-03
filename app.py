import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_icon='🍃', page_title='Text Generation Labeling Tool', layout='wide', initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>Text Generation Labeling Tool</h1>", unsafe_allow_html=True)

def file_selector(folder_path=r'./Datasets'):
    filenames = os.listdir(folder_path)
    return filenames, folder_path

def revert_question_type_id(txt_question_type):
    if txt_question_type == 'What':
        return 0
    elif txt_question_type == 'Who':
        return 1
    elif txt_question_type == 'When':
        return 2
    elif txt_question_type == 'Where':
        return 3
    elif txt_question_type == 'Why':
        return 4
    elif txt_question_type == 'How':
        return 5
    elif txt_question_type == 'Others':
        return 6

filenames, folder_path = file_selector()
filename_input = st.sidebar.selectbox(label='Input dataset file:', options=filenames)
df = pd.read_csv(f'./{folder_path}/{filename_input}')

if 'idx' not in st.session_state:
    st.session_state.idx = 0

st.markdown(f"<h4 style='text-align: center;'>Sample {st.session_state.idx + 1}/{len(df)}</h4>", unsafe_allow_html=True)

col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9, col_10 = st.columns([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

btn_previous = col_1.button(label=':arrow_backward: Previous sample', use_container_width=True)
btn_next = col_2.button(label='Next sample :arrow_forward:', use_container_width=True)
btn_save = col_3.button(label=':heavy_check_mark: Save change', use_container_width=True)
txt_goto = col_4.selectbox(label='Sample', label_visibility='collapsed', options=list(range(1, len(df) + 1)))
btn_goto = col_5.button(label=':fast_forward: Move to', use_container_width=True)

if len(df) != 0:
    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8, col_9, col_10 = st.columns(spec=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    txt_context = st.text_area(height=200, label='Your context:', value=df['context'][st.session_state.idx])

    col_11, col_12, col_13 = st.columns([4.5, 1, 4.5])
    txt_question = col_11.text_area(height=90, label='Your question:', value=df['question'][st.session_state.idx])
    txt_question_type = col_12.selectbox(label='Your question type:', options=['What', 'Who', 'When', 'Where', 'Why', 'How', 'Others'], index=int(df['question_type'][st.session_state.idx]))
    txt_answer = col_13.text_area(height=90, label='Your answer:', value=df['answer'][st.session_state.idx])

    st.markdown(f"<p style='text-align: left; font-weight: normal; font-size: 14px'>Your distractors:</p>", unsafe_allow_html=True)

    col_21, col_22 = st.columns(spec=[9, 1])
    txt_distractors = col_21.text_area(height=90, label='Your distractors:', label_visibility='collapsed', value=df['distract'][st.session_state.idx])  
    btn_generate_distractor = col_22.button(label='Generate distractors', use_container_width=True)
    
    if btn_generate_distractor:
        if filename_input == 'BiologyQA.csv':
            expert = 'biologist'
        elif filename_input == 'GeographyQA.csv':
            expert = 'geographer'
        elif filename_input == 'HistoryQA.csv':
            expert = 'historian'
        url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'
        headers = {'Content-Type': 'application/json'}
        data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': f"You are a great {expert}, here is the following content: context: '{txt_context}', question: '{txt_question}', answer: '{txt_answer}' generate three distract answers. Distractor answers are separated by [SEP]. Example: Distract answer 1 [SEP] Distract answer 2 [SEP] Distract answer 3"
                        }
                    ]
                }
            ]
        }
        api_key = 'AIzaSyApFAbCUA1H-VHAidzqmyStHFe92ODeO1Y'
        params = {'key': api_key}
        response = requests.post(url, headers=headers, json=data, params=params)
        if response.status_code == 200:
            correct = response.json()['candidates'][0]['content']['parts'][0]['text']
            st.success(f'3 distraction answers: {correct}')
            st.cache_data.clear()
        else:
            st.error('Failed to generate distractors. Please check API and inputs.')
            st.rerun()

    if btn_previous:
        if st.session_state.idx > 0:
            st.session_state.idx -= 1
            st.rerun()
        else:
            pass

    if btn_next:
        if st.session_state.idx < (len(df) - 1):
            st.session_state.idx += 1
            st.rerun()
        else:
            pass

    if btn_save:
        df['context'][st.session_state.idx] = txt_context
        df['question'][st.session_state.idx] = txt_question
        df['answer'][st.session_state.idx] = txt_answer
        df['distract'][st.session_state.idx] = txt_distractors
        df['question_type'][st.session_state.idx] = revert_question_type_id(txt_question_type)

        df.to_csv(f'./Datasets/{filename_input}', index=None)

    if btn_goto:
        st.session_state.idx = txt_goto - 1
        st.rerun()
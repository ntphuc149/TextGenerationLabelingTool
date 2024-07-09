import streamlit as st
import pandas as pd
import os
import requests

st.set_page_config(page_icon='🍃', page_title='Text Generation Labeling Tool by n.t.phuc149 🌒', layout='wide', initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center;'>Text Generation Labeling Tool by n.t.phuc149 🌒</h1>", unsafe_allow_html=True)

def file_selector(folder_path=r'./DemoDatasets'):
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
st.sidebar.markdown("<h1 style='text-align: center;'>QAD EVALUATION METRICS</h1>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align: left;'>☑️ Question Evaluation metrics</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>1. [Q] Fluency</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá mức độ trôi chảy của câu hỏi, tức là câu hỏi được diễn đạt một cách mượt mà, dễ hiểu, và tự nhiên.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu hỏi khó hiểu, không trôi chảy, có cấu trúc ngữ pháp lỗi thời hoặc sai lệch, khiến người đọc khó theo dõi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu hỏi hơi lủng củng nhưng miễn cưỡng hiểu được.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu hỏi được diễn đạt một cách mượt mà, không có lỗi ngữ pháp, dễ hiểu và dễ theo dõi.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>2. [Q] Clarity</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá mức độ rõ ràng của câu hỏi, liệu câu hỏi có cung cấp đủ thông tin để người đọc hiểu rõ vấn đề đang được hỏi không.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu hỏi mơ hồ, thiếu thông tin cần thiết để hiểu được vấn đề, hoặc sử dụng từ ngữ khiến người đọc bối rối.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu hỏi có thể được hiểu, nhưng có thể gây nhầm lẫn hoặc cần một số suy luận để làm rõ ý.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu hỏi rõ ràng, dễ hiểu, trực tiếp đưa ra hoặc yêu cầu thông tin cụ thể mà không gây nhầm lẫn.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>3. [Q] Conciseness</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá mức độ ngắn gọn của câu hỏi, liệu câu hỏi có được trình bày một cách tinh gọn, không lan man hoặc dư thừa từ ngữ không.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu hỏi dài dòng, có nhiều thông tin không cần thiết hoặc lặp lại làm mất điểm tập trung của câu hỏi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu hỏi tương đối ngắn gọn nhưng vẫn còn một vài chi tiết không cần thiết có thể loại bỏ để làm cho câu hỏi được súc tích hơn.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu hỏi được trình bày một cách ngắn gọn, chỉ chứa thông tin cần thiết để hiểu và trả lời câu hỏi một cách đầy đủ.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align: left;'>☑️ Question & Answer Evaluation metrics</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>1. [QA] Relevance</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá liệu câu hỏi có liên quan đến context không và có yêu cầu thông tin chính từ context đó không.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu hỏi không liên quan đến nội dung của context, hoặc yêu cầu thông tin không xuất hiện trong context.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu hỏi có liên quan nhưng không trực tiếp yêu cầu thông tin chính hoặc cốt lõi của context.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu hỏi trực tiếp liên quan và yêu cầu thông tin chính hoặc quan trọng từ context.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>2. [QA] Consistency</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Tiêu chí này đánh giá mức độ nhất quán giữa nội dung câu hỏi với thông tin trong context, đảm bảo không xuất hiện mâu thuẫn hay thông tin không có cơ sở (tưởng tượng).</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu hỏi chứa nội dung mâu thuẫn hoặc không phù hợp với bất kỳ thông tin nào có trong context. Câu hỏi tạo ra thông tin mới không được đề cập hoặc không có cơ sở từ context.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu hỏi chủ yếu nhất quán với thông tin trong context nhưng có một số chi tiết nhỏ không hoàn toàn chính xác hoặc phù hợp. Những chi tiết này có thể gây nhầm lẫn hoặc suy đoán nhưng không làm thay đổi ý nghĩa tổng thể.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu hỏi hoàn toàn phù hợp và nhất quán với context, không có bất kỳ sự mâu thuẫn hay thông tin tưởng tượng nào.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>3. [QA] Answer Correctness</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Câu trả lời có đúng hay không.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu trả lời không chính xác, chứa nhiều thông tin sai lệch hoặc không liên quan đến câu hỏi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu trả lời có một số thông tin đúng, nhưng cũng có những sai sót hoặc phần không liên quan đến câu hỏi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu trả lời chính xác và đầy đủ, không có lỗi và hoàn toàn liên quan đến câu hỏi của mô hình được đặt ra.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>4. [QA] Answer Consistency</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá liệu câu hỏi có thể được trả lời bằng câu trả lời được cung cấp không.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu trả lời cung cấp không phù hợp hoặc không trả lời được câu hỏi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu trả lời phần nào đáp ứng được câu hỏi nhưng không hoàn toàn chính xác hoặc thiếu chi tiết.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu trả lời chính xác, đầy đủ và trực tiếp trả lời câu hỏi một cách rõ ràng.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align: left;'>☑️ Distractions Evaluation metrics</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>1. [D] Correctness</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá liệu các câu trả lời gây nhiễu có chính xác với câu hỏi được đưa ra, và nếu chúng sai, chúng phải sai một cách hợp lý.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu trả lời gây nhiễu hoàn toàn không liên quan hoặc sai một cách rõ ràng, không thể hiện sự hiểu biết về nội dung câu hỏi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu trả lời gây nhiễu có thể liên quan nhưng dễ dàng phân biệt là sai hoặc không phải là câu trả lời chính xác nhất.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu trả lời gây nhiễu là sai nhưng sai một cách hợp lý, có thể khiến người kiểm tra nhầm lẫn hoặc suy nghĩ kỹ lưỡng để loại bỏ.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>2. [D] Understanding</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá liệu các câu trả lời gây nhiễu có phản ánh sự hiểu biết sâu sắc về nội dung câu hỏi, khiến chúng trở thành những lựa chọn hợp lý.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu trả lời gây nhiễu không thể hiện bất kỳ hiểu biết nào về câu hỏi.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu trả lời gây nhiễu thể hiện một mức độ hiểu biết nhưng không đủ sâu sắc.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu trả lời gây nhiễu thể hiện hiểu biết tốt, khiến cho câu trả lời có vẻ như một lựa chọn hợp lý.</h4>", unsafe_allow_html=True)

st.sidebar.markdown("<h3 style='text-align: left; color: #B300A6; font-weight: bold; font-style: italic'>3. [D] Difficulty</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>- Đánh giá mức độ khó của các câu trả lời gây nhiễu, liệu chúng có yêu cầu suy nghĩ sâu sắc và phân biệt kỹ lưỡng từ người kiểm tra không.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ BAD: Câu trả lời gây nhiễu quá đơn giản, dễ dàng loại bỏ.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ ACCEPTABLE: Câu trả lời gây nhiễu có độ khó tương đối, yêu cầu một ít suy nghĩ nhưng không quá thách thức.</h4>", unsafe_allow_html=True)
st.sidebar.markdown("<h4 style='text-align: justify;'>+ GOOD: Câu trả lời gây nhiễu khó, yêu cầu suy nghĩ kỹ càng và khả năng phân tích tốt để phân biệt với câu trả lời đúng.</h4>", unsafe_allow_html=True)

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

    col_eval_1, col_eval_2, col_eval_3, col_eval_4, col_eval_5 = st.columns(spec=[1, 1, 1, 1, 1])

    options = ['UNRATED', 'BAD', 'ACCEPTABLE', 'GOOD']
    q_fluency_value = df['q_fluency'][st.session_state.idx]
    q_clarity_value = df['q_clarity'][st.session_state.idx]
    q_conciseness_value = df['q_conciseness'][st.session_state.idx]

    qa_relevance_value = df['qa_relevance'][st.session_state.idx]
    qa_consistency_value = df['qa_consistency'][st.session_state.idx]
    qa_answer_correctness_value = df['qa_answer_correctness'][st.session_state.idx]
    qa_answer_consistency_value = df['qa_answer_consistency'][st.session_state.idx]

    d_correctness_value = df['d_correctness'][st.session_state.idx]
    d_understanding_value = df['d_understanding'][st.session_state.idx]
    d_difficulty_value = df['d_difficulty'][st.session_state.idx]
    
    q_fluency = col_eval_1.selectbox(label='[Q] Fluency:', options=options, index=options.index(q_fluency_value))
    q_clarity = col_eval_2.selectbox(label='[Q] Clarity:', options=options, index=options.index(q_clarity_value))
    q_conciseness = col_eval_3.selectbox(label='[Q] Conciseness:', options=options, index=options.index(q_conciseness_value))

    qa_relevance = col_eval_4.selectbox(label='[QA] Relevance:', options=options, index=options.index(qa_relevance_value))
    qa_consistency = col_eval_5.selectbox(label='[QA] Consistency:', options=options, index=options.index(qa_consistency_value))
    qa_answer_correctness = col_eval_1.selectbox(label='[QA] Answer correctness:', options=options, index=options.index(qa_answer_correctness_value))
    qa_answer_consistency = col_eval_2.selectbox(label='[QA] Answer consistency:', options=options, index=options.index(qa_answer_consistency_value))

    
    d_correctness = col_eval_3.selectbox(label='[D] Correctness:', options=options, index=options.index(d_correctness_value))
    d_understanding = col_eval_4.selectbox(label='[D] Understanding:', options=options, index=options.index(d_understanding_value))
    d_difficulty = col_eval_5.selectbox(label='[D] Difficulty:', options=options, index=options.index(d_difficulty_value))

    if btn_generate_distractor:
        if filename_input == 'BiologyQA_demo.csv':
            expert = 'biologist'
        elif filename_input == 'GeographyQA_demo.csv':
            expert = 'geographer'
        elif filename_input == 'HistoryQA_demo.csv':
            expert = 'historian'
        elif filename_input == 'CivicEduQA_demo.csv':
            expert = 'civic educator'
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

        df['q_fluency'][st.session_state.idx] = q_fluency
        df['q_clarity'][st.session_state.idx] = q_clarity
        df['q_conciseness'][st.session_state.idx] = q_conciseness

        df['qa_relevance'][st.session_state.idx] = qa_relevance
        df['qa_consistency'][st.session_state.idx] = qa_consistency
        df['qa_answer_correctness'][st.session_state.idx] = qa_answer_correctness
        df['qa_answer_consistency'][st.session_state.idx] = qa_answer_consistency

        df['d_correctness'][st.session_state.idx] = d_correctness
        df['d_understanding'][st.session_state.idx] = d_understanding
        df['d_difficulty'][st.session_state.idx] = d_difficulty

        df.to_csv(f'./DemoDatasets/{filename_input}', index=None, encoding='utf-8-sig')
        st.rerun()

    if btn_goto:
        st.session_state.idx = txt_goto - 1
        st.rerun()

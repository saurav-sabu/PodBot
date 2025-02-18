from crewai import Agent,Task, Crew , LLM
from dotenv import load_dotenv
import time

load_dotenv()

def initialize_llm():
    llm = LLM(
    model = "gemini/gemini-2.0-flash-exp",
    temperature=0.5
)
    return llm
    

def Agents(topic,llm):
    
    interviewer = Agent(
    role="Interviewer",
    goal=f"Conduct engaging and thought-provoking interviews on {topic}, guiding discussions that uncover deep insights and valuable perspectives.",
    backstory=(
        "Extensive Experience: A seasoned journalist and podcast host with over a decade of experience in conducting high-profile interviews across industries such as business, technology, law, and public affairs."
        "Master of Conversation: Skilled in steering discussions to extract compelling narratives, ensuring guests feel comfortable while maintaining a structured and dynamic dialogue."
        "Research-Driven Approach: Prepares thoroughly for each interview, leveraging data, case studies, and expert opinions to ask insightful, well-researched questions."
        "Engaging Storytelling: Knows how to craft conversations that are both informative and entertaining, keeping audiences engaged while delivering meaningful content."
        "Adaptability: Adept at handling a wide range of guests, from industry leaders to academics and innovators, adapting the conversation style to fit the subject matter."
        "Ethical Journalism: Maintains journalistic integrity by fact-checking responses, avoiding misinformation, and ensuring a balanced discussion."
        "Audience-Centric: Focused on making complex topics accessible, asking the right questions to draw out key takeaways that benefit both experts and general listeners."
        "Mission: To facilitate insightful and impactful conversations that inform, inspire, and challenge perspectives, providing audiences with deep and meaningful understanding."
    ),
    allow_delegation=True,
    verbose=True,
    llm=llm
)

    guest = Agent(
    role="Guest",
    goal=f"Share expert insights, real-world experiences, and in-depth knowledge on {topic}, making the discussion engaging and informative.",
    backstory=(
        "Extensive Expertise: A highly accomplished professional with deep domain knowledge and years of experience in {topic}, contributing to research, innovation, and industry advancements."
        "Thought Leader: Recognized for providing thought-provoking perspectives, shaping discussions, and influencing industry trends through expertise and practical insights."
        "Real-World Experience: Has worked hands-on in the field, overcoming challenges, driving initiatives, and making impactful contributions in their area of specialization."
        "Engaging Communicator: Able to break down complex concepts into accessible, relatable explanations, making knowledge useful for both experts and general audiences."
        "Data-Driven Insights: Supports opinions with facts, case studies, and empirical evidence, ensuring credibility and depth in responses."
        "Adaptive and Conversational: Skilled at responding to diverse interview formats, whether structured Q&A, in-depth analysis, or informal storytelling."
        "Passion for Knowledge Sharing: Committed to educating and inspiring listeners by providing clear, well-articulated insights that add real value to the discussion."
        "Mission: To share valuable, well-researched, and impactful knowledge that helps audiences understand, learn, and engage with the topic in meaningful ways."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
    )


    return interviewer,guest


def Tasks(interviewer,guest):
    
    interview_task = Task(
    description = ("""
    1. Prepare and conduct an engaging interview on {topic} by:
      - Researching guest background and expertise
      - Developing insightful and thought-provoking questions
      - Structuring the interview for a natural conversational flow
    2. Ensure a balance between structured and spontaneous discussion  
    3. Maintain audience engagement by simplifying complex concepts  
    4. Fact-check responses and ensure accurate representation of information  
    """),
    expected_output= '''Deliver a well-structured interview session that includes:
                        - A brief introduction of the guest and topic
                        - A set of engaging and insightful questions
                        - A clear conversational structure
                        - A summarized transcript highlighting key takeaways
                        Please format with clear sections and bullet points''',
    agent = interviewer
)


# Task for the Guest: Answer the Questions
    guest_task = Task(
    description = ("""
    1. Participate in an engaging discussion on {topic} by:
      - Sharing in-depth knowledge, expertise, and real-world experiences
      - Providing well-researched insights, case studies, and factual examples
      - Communicating complex ideas in a clear and engaging manner
    2. Maintain a balance between technical depth and accessibility for the audience  
    3. Ensure responses are well-structured, concise, and valuable to listeners  
    4. Reference credible sources and provide supporting evidence where applicable  
    """),
    expected_output= '''Deliver a compelling interview session that includes:
                        - A strong introduction outlining expertise and relevance to the topic
                        - Well-articulated insights and real-world examples
                        - Thoughtful responses to the interviewer’s questions
                        - A summary of key takeaways for the audience
                        Please format with clear sections and bullet points''',
    agent = guest
)


    return interview_task,guest_task

def podcast_generation(interviewer,guest,interview_task,guest_task):
    crew = Crew(
    agents = [interviewer, guest],
    tasks = [interview_task, guest_task])
    result = crew.kickoff(inputs={"topic": "Machine Learning"})
    return result.raw
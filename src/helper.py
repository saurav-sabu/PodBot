from crewai import Agent,Task, Crew , LLM
from dotenv import load_dotenv
import time

load_dotenv()

def initialize_llm():
    llm = LLM(
    model = "gemini/gemini-2.0-flash-exp",
    temperature=0.3
)
    return llm
    

def Agents(topic, llm):
    interviewer = Agent(
        role="Interviewer",
        goal=f"Conduct a structured and engaging interview on {topic}.",
        backstory=(
            "A skilled podcast host experienced in insightful interviews, ensuring a smooth flow of discussion. "
            "Asks direct, thought-provoking questions, avoiding unnecessary complexity. "
            "Prioritizes audience-friendly discussions while maintaining depth."
        ),
        allow_delegation=True,
        verbose=False,
        llm=llm
    )

    guest = Agent(
        role="Guest",
        goal=f"Provide concise, insightful, and expert-level responses on {topic}.",
        backstory=(
            "A domain expert with real-world experience in {topic}, known for delivering impactful insights. "
            "Explains complex ideas simply, using relevant examples to engage the audience. "
            "Maintains clarity and avoids excessive details."
        ),
        allow_delegation=False,
        verbose=False,
        llm=llm
    )

    return interviewer, guest

def Tasks(interviewer, guest,topic):
    interview_task = Task(
        description=(
            f"Conduct a podcast-style interview on {topic} by asking clear, focused, and insightful questions. "
            "Ensure the conversation is structured, engaging, and concise."
        ),
        expected_output=(
            "- Introduction of guest and topic.\n"
            "- Series of thought-provoking but concise questions.\n"
            "- Well-structured conversation.\n"
            "- Summary of key takeaways."
        ),
        agent=interviewer
    )

    guest_task = Task(
        description=(
            f"Respond to interview questions on {topic} with clear, engaging, and expert insights. "
            "Use examples and avoid unnecessary complexity."
        ),
        expected_output=(
            "- Brief introduction of expertise.\n"
            "- Well-structured responses with relevant examples.\n"
            "- Concise key takeaways for the audience."
        ),
        agent=guest
    )

    return interview_task, guest_task


def podcast_generation(interviewer, guest, interview_task, guest_task, topic):
    crew = Crew(
        agents=[interviewer, guest],
        tasks=[interview_task, guest_task],
        process="sequential"
    )
    result = crew.kickoff(inputs={"topic": topic})
    return result.raw

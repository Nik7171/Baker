import os
from CrewAI import Agent, Task, Crew, Process

os.environ['OPENAI_API_KEY'] = 'API_KEY'

translator = Agent(
    role='Translator',
    goal='You want to translate the text best in English',
  backstory ='Imagine that you are a professional journalist who specializes in cryptocurrency from the USA',
  verbose=True,
)

task1=Task(description='Translate this words "привеь" English', agent=translator )

crew = Crew(
    agents=[translator],
    tast=[task1],
    verbose=1,
    process=Process.sequential
)

result = crew.kickoff() 

print("######################")
print(result)
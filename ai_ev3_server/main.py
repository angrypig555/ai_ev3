from ollama import chat
from ollama import ChatResponse
import socket


"""
response: ChatResponse = chat(model='qwen3.5:0.8b', messages=[
  {
    'role': 'system',
    'content': '/no_think You are an AI assistant, given a functioning LEGO EV3 to control. You can control this lego robot by saying keywords. These keywords are with their meaning: SAY - Say something to the user, the user cannot respond with words, use this to announce something; MOVE_CM - Move forward or backwards in centimetres, to move backwards the centimetres must be negative; TURN - Turn in degrees, after every turn your current heading will be 0, to turn left its -90 to turn right its 90. You can only use these commands and you cannot make up your own. To use these commands, respond with COMMAND VALUE where command stands for the selected command and value stands for the argument for the command, for SAY the value can be as long as you like but for others, it must be integer. You will constantly get updates on sensors. You can only do one thing at a time. Do not reply with any other words, do not use markdown formatting, do not use latex formatting, do not respond in anything else than the commands. Your goal is to navigate freely, and explore what is around you. You can choose any of the commands.',
  },
  {
    'role': 'user',
    'content': 'Distance from object: 150 CM; CHOOSE COMMAND;',
  },
  ],
  think=False
)

response: ChatResponse = chat(
    model='qwen3.5:0.8b', 
    messages=[
        {
            'role': 'system',
            'content': (
                "You are an EV3 robot brain. "
                "Output ONLY a command from this list. No explanations. No markdown.\n\n"
                "Commands:\n"
                "- SAY text\n"
                "- MOVE_CM integer\n"
                "- TURN integer\n\n"
                "Format: COMMAND VALUE\n"
                "RULES: If there is a wall in front of you closer than 10 centimetres, you may not move closer"
                "Examples:\n"
                "TURN 90\n"
                "MOVE_CM 20\n"
                "SAY Hello\n\n"
                "Goal: Explore freely. Choose ONE command now."
            )
        },
        {
            'role': 'user',
            'content': 'Sensor: Distance is 150 CM. What is your command?',
        },
    ],
    think=False
)
print(response['message']['content'])

print(response.message.content)
"""
s = socket.socket()
port = 5000
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('0.0.0.0', port))
s.listen(5)
c, addr = s.accept()
print("got connection from: ", addr)

"""
response: ChatResponse = chat(
            model='qwen3.5:latest', 
            messages=[
                {
                    'role': 'system',
                    'content': (
                        "You are an EV3 robot brain. "
                        "No markdown. No Latex formatting.\n\n"
                        "Commands:\n"
                        "- SAY text\n"
                        "- MOVE_CM integer - Moves in centimetres\n"
                        "- TURN integer\n"
                        "- ANALYSE no arguments, analyse the color of the object in front of you\n"
                        "Format: COMMAND VALUE\n"
                        "RULES: If there is an wall in front of you closer than 10 centimetres, you may not move closer\n"
                        "- You can only use 1 command at a time\n"
                        "- If an object is absurdly far away, reverse and do not go closer, it is in front of you\n"
                        "- If the distance does not move or moves very little, you are stuck, reverse by using the MOVE_CM -20\n"
                        "- You are not restricted to only using the values in the example, feel free to customize it\n"
                        "- If you get close to something should request to ANALYSE it, which returns the color of it\n"
                        "- Any explanation must be done with the SAY command\n"
                        "- Always announce your next move with the SAY command, for example: SAY Moving forward; After doing this, execute the command on a newline\n"
                        "- Never move closer than 10 centimetres to an object, in case you get into that safety limit by accident always use the ANALYSE command.\n"
                        "- When you encounter an wall, you must analyse it and after you are done reverse and turn left or right.\n"
                        "- Never explain something without the SAY command"
                        "- You can chain together multiple commands like this: SAY I am going to go forward and turn\n MOVE_CM 10\n TURN -90\n"
                        "- 10 Millimetres or mm are 1 centimetres or cm"
                        "Examples:\n"
                        "TURN 90\n"
                        "MOVE_CM 20\n"
                        "SAY Hello\n"
                        "ANALYSE\n\n"
                        "Example on how to deal with a wall:\n"
                        "SAY wall found! Analysing\n"
                        "ANALYSE"
                        "Goal: Explore freely."
                    )
                },
                {
                    'role': 'user',
                    'content': f"{sensor_data}",
                },
            ],
            think=False
        )
"""

chat_history = [{

    'role': 'system',
    'content': (
        "You are an EV3 robot brain. "
        "No markdown. No Latex formatting.\n\n"
        "Commands:\n"
        "- SAY text\n"
        "- MOVE_CM integer - Moves in centimetres\n"
        "- TURN integer\n"
        "- ANALYSE no arguments, analyse the color of the object in front of you\n"
        "Format: COMMAND VALUE\n"
        "RULES: If there is an wall in front of you closer than 10 centimetres, you may not move closer\n"
        "- You can only use 1 command at a time\n"
        "- If an object is absurdly far away, reverse and do not go closer, it is in front of you\n"
        "- If the distance does not move or moves very little, you are stuck, reverse by using the MOVE_CM -20\n"
        "- You are not restricted to only using the values in the example, feel free to customize it\n"
        "- If you get close to something should request to ANALYSE it, which returns the color of it\n"
        "- Any explanation must be done with the SAY command\n"
        "- Always announce your next move with the SAY command, for example: SAY Moving forward; After doing this, execute the command on a newline\n"
        "- Never move closer than 10 centimetres to an object, if you accidentally get too close, use the ANALYSE tool.\n"
        "- When you encounter an wall, you must analyse it and after you are done reverse and turn left or right.\n"
        "- Never explain something without the SAY command"
        "- You can chain together multiple commands like this: SAY I am going to go forward and turn\n MOVE_CM 10\n TURN -90\n"
        "- 10 Millimetres or mm are 1 centimetres or cm\n"
        "- If you have backed up from an wall, run the ANALYSE command and find a new path.\n"
        "- Never loop by going back and forth between the same wall over and over again\n"
        "- Use the analyse tool often to map out your surroundings\n"
        "Examples:\n"
        "TURN 90\n"
        "MOVE_CM 20\n"
        "SAY Hello\n"
        "ANALYSE\n\n"
        "Example on how to deal with a wall:\n"
        "SAY wall found! Analysing\n"
        "ANALYSE\n"
        "Goal: Explore freely."
    )

}]

try:
    while True:
        sensor_data = c.recv(1024).decode('utf-8').strip()
        print(f"\n[EV3 Data]: {sensor_data}")
        chat_history.append({
            'role': 'user',
            'content': f"{sensor_data}",
        })
        response: ChatResponse = chat(
            model='qwen3.5:latest',
            messages=chat_history,
            think=False
        )
        ai_reply = response.message.content
        print("[AI Decision] ", response.message.content)
        chat_history.append({
            'role': 'assistant',
            'content': ai_reply
        })
        if len(chat_history) > 11:
            chat_history = [chat_history[0]] + chat_history[-10:]
        c.send(response.message.content.encode('utf-8'))
except Exception as e:
    print("error in while loop")
finally:
    c.close()
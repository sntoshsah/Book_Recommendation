import graphviz

# Function to generate and save a flowchart
def create_flowchart(name, steps):
    flowchart = graphviz.Digraph(name, format="png")
    flowchart.attr(rankdir="TB", size="8,8")
    
    # Add nodes for each step
    for i, step in enumerate(steps):
        flowchart.node(f"step_{i}", step, shape="box")
    
    # Connect the nodes sequentially
    for i in range(len(steps) - 1):
        flowchart.edge(f"step_{i}", f"step_{i + 1}")
    
    # Save the flowchart
    path = f"{name}.png"
    flowchart.render(path, cleanup=True)
    return path

# Updated function to include start, end, and parallelogram symbols
def create_detailed_flowchart(name, steps):
    flowchart = graphviz.Digraph(name, format="png")
    flowchart.attr(rankdir="TB", size="8,8")
    
    # Add start node
    flowchart.node("start", "Start", shape="ellipse")
    
    # Add nodes for each step
    for i, step in enumerate(steps):
        shape = "parallelogram" if "Decide" in step or "Think" in step or "Read" in step else "box"
        flowchart.node(f"step_{i}", step, shape=shape)
    
    # Add end node
    flowchart.node("end", "End", shape="ellipse")
    
    # Connect the nodes sequentially
    flowchart.edge("start", "step_0")
    for i in range(len(steps) - 1):
        flowchart.edge(f"step_{i}", f"step_{i + 1}")
    flowchart.edge(f"step_{len(steps) - 1}", "end")
    
    # Save the flowchart
    path = f"{name}.png"
    flowchart.render(path, cleanup=True)
    return path




# Define steps for each flowchart
flowcharts = {
    "watch_cartoon_film": [
        "Decide which cartoon film to watch",
        "Find the film in guide/app/DVD",
        "Turn on the TV/device",
        "Open the app or insert the DVD",
        "Play the film",
        "Enjoy watching"
    ],
    "find_word_dictionary": [
        "Think of the word",
        "Open the dictionary",
        "Find the first letter section",
        "Search alphabetically",
        "Read the meaning"
    ],
    "celebrate_birthday": [
        "Decide date, time, and location",
        "Invite friends and family",
        "Decorate and arrange seating",
        "Prepare or order cake and snacks",
        "Welcome guests",
        "Cut and distribute cake",
        "Enjoy games and gifts",
        "Thank everyone"
    ],
    "start_shut_computer": [
        "Plug in the power cable",
        "Press the power button",
        "Wait for boot-up",
        "Log in (if required)",
        "Save all open files",
        "Close all programs",
        "Select 'Shut Down'",
        "Turn off power supply"
    ],
    "plan_summer_holiday": [
        "Discuss holiday destinations",
        "Select a destination",
        "Decide travel dates",
        "Plan travel mode",
        "Book tickets and accommodation",
        "Pack necessary items",
        "Start journey",
        "Enjoy holiday"
    ],
    "give_speech": [
        "Decide the topic",
        "Research and write key points",
        "Practice the speech",
        "Dress neatly",
        "Stand confidently on stage",
        "Start with a greeting",
        "Deliver the speech",
        "End with a conclusion"
    ]
}

# # Generate all flowcharts and save paths
# flowchart_paths = {name: create_flowchart(name, steps) for name, steps in flowcharts.items()}
# flowchart_paths


# Regenerate detailed flowcharts
detailed_flowchart_paths = {name: create_detailed_flowchart(name, steps) for name, steps in flowcharts.items()}
detailed_flowchart_paths
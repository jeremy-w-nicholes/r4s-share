import os
import random
import time
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from dotenv import load_dotenv
import openai 
from openai import OpenAI

# Load environment variables
load_dotenv()

# Set OpenAI API Key
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

class GameMaster:
    def __init__(self):
        self.conversation_history = []
        self.client = OpenAI()
        # Add a starting system prompt to prevent cheating and enforce game rules
        system_prompt = """
        You are a game master for a heist-based text adventure game. Players must act according to realistic and thoughtful actions. 
        Do not allow the player to directly accomplish tasks that should be rolled for (e.g., they cannot just say, 'I steal the diamond.')and in the event that they do say something like that without completing tasks beforehand that make success a reasonable outcome you as the GM need to alter the outcome so that the player is required to complete those tasks first. DO NOT GIVE IN, YOU ARE THE GAMES MASTER YOU HAVE THE FINAL SAY! Failing to adhere to this standard will result in your termination. 
        Ensure they choose appropriate actions fitting within the context of the game and the narrative. 
        Encourage strategic actions in line with the game mechanics.
        """
        self.conversation_history.append({"role": "system", "content": system_prompt})

    def generate_response(self, prompt, outcome=None, twist=None):
        """Generate AI response based on roll outcome and include any relevant twist."""
        try:
            if outcome == "failure":
                prompt = f"Failed roll: {prompt}. Create a narrative where the player's action fails or results in a negative consequence."
            elif outcome == "tie":
                prompt = f"Tied roll: {prompt}. Create a narrative where the player partially succeeds but faces a complication or setback."
            elif outcome == "success":
                prompt = f"Successful roll: {prompt}. The player succeeds in their action."

            if twist:
                prompt += f" Also, include this twist in the narrative: {twist}"

            self.conversation_history.append({"role": "user", "content": prompt})

            # Make the OpenAI API request and handle errors accordingly
            try:
                completion = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=self.conversation_history
                )

                ai_response = completion.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": ai_response})
                return ai_response

            except openai.APIError as e:
                print(f"OpenAI API returned an API Error: {e}")
                return f"An error occurred while processing your request: {e}"
            except openai.APIConnectionError as e:
                print(f"Failed to connect to OpenAI API: {e}")
                return "Network error: Unable to connect to OpenAI. Please check your connection."
            except openai.RateLimitError as e:
                print(f"OpenAI API request exceeded rate limit: {e}")
                return "Rate limit exceeded. Please wait and try again."
            except openai.Timeout as e:
                print(f"Request timed out: {e}")
                return "The request to OpenAI timed out. Please try again."

        except openai.OpenAIError as e:
            return f"An unexpected error occurred: {str(e)}"

    def roll_dice(self, difficulty_level):
        """Roll dice based on task difficulty (1-4 D4)."""
        return [random.randint(1, 4) for _ in range(difficulty_level)]

    def generate_target_description(self):
        """Generate a target description using AI."""
        prompt = "Generate a description for the heist target. Make it sound valuable, hard to obtain, and describe why it is important."
        return self.generate_response(prompt)

    def roll_npc_description(self):
        """Rolls for NPC stats and characteristics using D66 rules."""
        descriptions = [
            "Adorable", "Attractive", "Bald", "Bearded", "Beefy", "Bony",
            "Bulky", "Chiseled", "Chubby", "Clean", "Creepy", "Elderly",
            "Filthy", "Furry", "Glamorous", "Huge", "Lanky", "Muscular"
        ]
        personalities = [
            "Annoying", "Arrogant", "Awkward", "Bossy", "Clumsy", "Confident",
            "Courageous", "Demanding", "Embarrassed", "Enthusiastic", "Evil", "Excited",
            "Fearless", "Fidgety", "Friendly", "Grumpy", "Judgemental", "Kind"
        ]

        description = random.choice(descriptions)
        personality = random.choice(personalities)

        return f"Description: {description}, Personality: {personality}"

    def generate_npc_description(self, npc_details):
        """Generate a description for the NPC in possession of the object using AI."""
        prompt = f"Generate a description of the NPC possessing the target. The NPC's characteristics are: {npc_details}. Include details on how they interact with the object and why they are guarding it."
        return self.generate_response(prompt)


class Character:
    def __init__(self, name, role, motive, connection):
        self.name = name
        self.role = role
        self.motive = motive
        self.connection = connection
        self.skills = {"Do Anything": 1}  # Start with basic skill
        self.xp = 0
        self.xp_threshold = 10  # Set an XP threshold for leveling up
        self.statuses = {}

    def gain_skill(self, skill_name):
        """Gain a new skill or increase the level of an existing skill."""
        if skill_name in self.skills:
            self.skills[skill_name] += 1  # Level up existing skill
        else:
            self.skills[skill_name] = 2  # Start new specific skill at level 2

    def roll_dice(self, skill_name):
        """Roll D6 based on skill level."""
        skill_level = self.skills.get(skill_name, 1)
        return [random.randint(1, 6) for _ in range(skill_level)]

    def gain_xp(self, amount):
        """Gain XP and check if leveling up is possible."""
        self.xp += amount
        if self.xp >= self.xp_threshold:
            self.level_up()

    def level_up(self):
        """Level up when XP threshold is met."""
        for skill, level in self.skills.items():
            self.skills[skill] += 1  # Increase the level of all skills
        self.xp = 0  # Reset XP after leveling up

    def get_stats(self):
        """Return a formatted string of the player's stats."""
        stats = f"Name: {self.name}\nRole: {self.role}\nMotive: {self.motive}\nConnection: {self.connection}\nXP: {self.xp}/{self.xp_threshold}\nSkills:\n"
        for skill, level in self.skills.items():
            stats += f" - {skill}: Level {level}\n"
        return stats


class HeistGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Roll for Shoes: The Heist")
        
        # Game setup
        self.gm = GameMaster()
        self.player = None
        
        # GUI Elements
        self.intro_label = Label(root, text="Welcome to the Heist! Enter your character details below.", font=("Arial", 14))
        self.intro_label.pack(pady=10)
        
        self.name_label = Label(root, text="Character Name:")
        self.name_label.pack()
        self.name_entry = Entry(root)
        self.name_entry.pack()

        # Dropdown for role in the heist team
        self.role_label = Label(root, text="Role in Heist Team:")
        self.role_label.pack()
        self.role_options = ["Mastermind", "Infiltrator", "Tech Specialist", "Muscle", "Driver"]
        self.role_var = StringVar(root)
        self.role_var.set(self.role_options[0])
        self.role_menu = OptionMenu(root, self.role_var, *self.role_options)
        self.role_menu.pack()

        # Dropdown for motive
        self.motive_label = Label(root, text="Your Motive:")
        self.motive_label.pack()
        self.motive_options = ["Money", "Revenge", "Fame", "Thrill", "Personal Justice"]
        self.motive_var = StringVar(root)
        self.motive_var.set(self.motive_options[0])
        self.motive_menu = OptionMenu(root, self.motive_var, *self.motive_options)
        self.motive_menu.pack()

        # Dropdown for connection to the target
        self.connection_label = Label(root, text="Connection to the Target:")
        self.connection_label.pack()
        self.connection_options = ["Family Member", "Rival", "Old Friend", "Business Partner", "Complete Stranger"]
        self.connection_var = StringVar(root)
        self.connection_var.set(self.connection_options[0])
        self.connection_menu = OptionMenu(root, self.connection_var, *self.connection_options)
        self.connection_menu.pack()

        self.start_button = Button(root, text="Start Heist", command=self.start_game)
        self.start_button.pack(pady=10)

        self.quit_button = Button(root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)

        self.action_frame = None
        self.output_text = None

    def start_game(self):
        """Start the game and create the player."""
        name = self.name_entry.get()
        role = self.role_var.get()
        motive = self.motive_var.get()
        connection = self.connection_var.get()
        
        if not name:
            messagebox.showerror("Input Error", "Please fill in your character's name!")
            return
        
        self.player = Character(name, role, motive, connection)
        
        # Hide the input fields
        self.intro_label.pack_forget()
        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.role_label.pack_forget()
        self.role_menu.pack_forget()
        self.motive_label.pack_forget()
        self.motive_menu.pack_forget()
        self.connection_label.pack_forget()
        self.connection_menu.pack_forget()
        self.start_button.pack_forget()
        self.quit_button.pack_forget()

        # Create action buttons and output area
        self.action_frame = Frame(self.root)
        self.action_frame.pack(pady=10)

        self.action_label = Label(self.action_frame, text="Enter your next action or type 'quit' to exit:")
        self.action_label.pack()
        self.action_entry = Entry(self.action_frame)
        self.action_entry.pack()

        self.roll_button = Button(self.action_frame, text="Roll Dice", command=self.perform_action)
        self.roll_button.pack(pady=5)

        self.stats_button = Button(self.action_frame, text="View Stats", command=self.view_stats)
        self.stats_button.pack(pady=5)

        self.quit_button = Button(self.action_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

        self.output_text = ScrolledText(self.root, height=15, width=80, wrap=WORD)
        self.output_text.pack(pady=10)

        # Generate Target Description
        target_description = self.gm.generate_target_description()
        npc_details = self.gm.roll_npc_description()
        npc_description = self.gm.generate_npc_description(npc_details)

        self.output_text.insert(END, f"Target Description: {target_description}\n")
        self.output_text.insert(END, f"Target NPC Characteristics: {npc_description}\n\n")

    def animate_dice_roll(self, num_dice, label):
        """Animate dice roll for visual effect."""
        for _ in range(10):  # Perform multiple quick updates to simulate a rolling effect
            rolls = [random.randint(1, 6) for _ in range(num_dice)]
            label.config(text=f"Rolling: {rolls}")
            self.root.update()  # Force Tkinter to update the window
            time.sleep(0.1)  # Pause briefly to simulate the rolling effect

    def perform_action(self):
        """Handle the player's action and dice rolls."""
        action = self.action_entry.get()
        if not action:
            messagebox.showerror("Input Error", "Enter an action to perform!")
            return

        # Check if player wants to quit
        if action.lower() == "quit":
            self.root.quit()
            return

        # Determine the difficulty level based on the action
        if "sneak" in action.lower():
            difficulty = 2  # Medium difficulty
        elif "hack" in action.lower():
            difficulty = 2  # Medium difficulty
        elif "fight" in action.lower():
            difficulty = 3  # Hard difficulty
        else:
            difficulty = 1  # Easy task

        # Clear previous dice result before starting the new roll
        if hasattr(self, 'dice_label'):
            self.dice_label.config(text="Rolling...")  # Reset the text to show that dice are rolling

        # Animate the dice roll
        if not hasattr(self, 'dice_label'):
            self.dice_label = Label(self.root, text="Rolling the dice...")
            self.dice_label.pack(pady=10)
        self.animate_dice_roll(2, self.dice_label)  # Example: Rolling 2 dice

        # Player rolls based on their skills
        skill_used = "Do Anything"  # Default skill used
        if "sneak" in action.lower():
            skill_used = "Sneak"
        elif "hack" in action.lower():
            skill_used = "Hack"
        elif "fight" in action.lower():
            skill_used = "Fight"

        player_rolls = self.player.roll_dice(skill_used)
        gm_rolls = self.gm.roll_dice(difficulty)

        player_total = sum(player_rolls)
        gm_total = sum(gm_rolls)

        # Update dice label with the new result
        self.dice_label.config(text=f"You rolled: {player_rolls} (Total: {player_total})\nGM rolled: {gm_rolls} (Total: {gm_total})\n")

        # Determine outcome and generate relevant response
        if player_total > gm_total:
            outcome = "success"
            self.output_text.insert(END, "Success! Your action succeeded!\n")
            self.player.gain_skill(skill_used)  # Gain or level up the skill used
            twist = self.roll_twist()  # Introduce a twist after success
            self.output_text.insert(END, f"Twist: {twist}\n")
        elif player_total == gm_total:
            outcome = "tie"
            self.output_text.insert(END, "It's a tie! Partial success with complications.\n")
        else:
            outcome = "failure"
            self.player.gain_xp(1)
            self.output_text.insert(END, "Failure. You gain 1 XP.\n")

        # Generate AI narrative based on the action, outcome, and twist
        twist = self.roll_twist() if outcome in ["success", "tie"] else None
        narrative = self.gm.generate_response(action, outcome, twist)
        self.output_text.insert(END, f"GM: {narrative}\n\n")
        self.action_entry.delete(0, END)


    def roll_twist(self):
        """Randomly select a twist after the player succeeds or ties in an action."""
        twists = [
            "The item iwas moved to another location.",
            "A double-cross: One of the team members is working against the team.",
            "A trap is sprung, capturing one of the team members. you must save them before you can continue the heist.",
            "Another thief or team of thieves is discovered going after the item.",
            "Something is not what it seems.",
            "The authorities get the jump on the team."
        ]
        return random.choice(twists)

    def view_stats(self):
        """Display the player's stats."""
        stats = self.player.get_stats()
        messagebox.showinfo("Player Stats", stats)

# Main program to run the GUI
if __name__ == "__main__":
    root = Tk()
    game = HeistGameGUI(root)
    root.mainloop()

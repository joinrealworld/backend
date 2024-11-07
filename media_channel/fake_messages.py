from faker import Faker
import random

fake = Faker()

# Expanded elements for casual, friendly chat messages
greetings = [
    "Hey {name} 😊", "Yo {name}!", "Sup {name}?", "Heyy {name} 👋", "Hii {name}!",
    "Hola {name}!", "Heyyy!", "Hey {name}, wassup?", "Omg {name}, hii!", "Hellooo {name}!"
]

casual_starters = [
    "Real quick...", "Btw,", "Just thought of something...", "Got a sec?", "Sooo...",
    "Okay, hear me out...", "Not to bug ya but...", "Sooo, guess what?", "Random thought:",
    "Can I just say...", "Okay but like,", "Bruh,", "Umm, wait..."
]

main_messages = [
    "Did u check out that {topic} I sent?", "Are we still on for {time}?", "Wanna hang at {place} later?",
    "Can u believe {news}?", "Thoughts on {topic}?", "Yo, r u free at {time}?", "Any plans for {day}?",
    "So like, about {topic}...", "Pls send that {file} if u got it!", "Got any good recs for {thing}?",
    "Wanna catch up on {show}?", "Did u already finish {task}?", "Omg we NEED to talk about {topic} 😆",
    "Can we just talk about {topic} real quick?", "You gotta see this {thing} I found!"
]

follow_ups = [
    "Also, btw...", "Oh and btw,", "Just remembered...", "Like, fyi...", "Oh! one more thing...",
    "Anddd ofc,", "LOL also,", "So yeah,", "Also, heads up!", "Oh btw,", "And yeah,",
    "Just putting it out there,"
]

responses = [
    "Haha no way!", "Omg love it 😂", "I’ll hit you up when I’m done!", "LOL sounds good!",
    "Just finished that!", "All set on my end 👍", "Omg I’m obsessed with {thing} rn 😂",
    "Nah, didn’t get to it yet", "Ohhh nice!", "Same here lol", "Lemme know if u need anything",
    "That’s wild!", "Love it!!", "I can def check it out!", "I’ll let u know asap",
    "Let’s gooo 😆", "Say less!"
]

acknowledgments = [
    "Haha okay cool!", "Gotcha!", "Noted 👍", "Yesss, love it!", "Sounds good!", "No prob!",
    "Cool cool, got it!", "All good!", "Will do!", "Yup yup!", "Thanks, appreciate it!",
    "Got it, thx!", "Yepp, all clear!", "Noted, ty!", "For sure, thanks!"
]

closings = [
    "Catch ya later!", "Talk soon!", "Lemme know what’s up!", "Later, dude!", "Bye for now!",
    "Peace out!", "Hit me up if anything", "Catch ya later ✌️", "Alrighty, bye!",
    "Stay awesome!", "Cya!", "Take it easy!", "Kk, byee!", "Stay cool 😎", "Laters!",
    "Ttyl!", "Cheers!", "Adios!"
]

# Create a casual conversation template with placeholders
def create_casual_message():
    message = (
        f"{random.choice(greetings)} {random.choice(casual_starters)} {random.choice(main_messages)} "
        f"{random.choice(follow_ups)} {random.choice(responses)} {random.choice(acknowledgments)} "
        f"{random.choice(closings)}"
    )

    # Fill placeholders with realistic fake data
    return message.format(
        name=fake.first_name(),
        topic=fake.word(),
        time=fake.time(),
        place=fake.city(),
        news=fake.sentence(),
        day=fake.day_of_week(),
        file=fake.file_name(extension="pdf"),
        thing=fake.word(),
        show=fake.catch_phrase(),
        task=fake.bs(),
    )

# Generate a list of unique casual messages
def generate_casual_messages(num_messages=10000):
    messages = set()
    while len(messages) < num_messages:
        messages.add(create_casual_message())
    return list(messages)

# # Example usage
# messages = generate_casual_messages(10)  # Generate 10 for demonstration
# for msg in messages[:10]:  # Display the first 10
#     print(msg)

# Vocava

1. **User and Tutor Setup**: It initializes a 'user' object that stores the user's native language, target language, and
   fluency level. These are stored in the Streamlit session state to persist across reruns. A 'tutor' is also created
   using an API key. The tutor model can be switched between "Claude" and "mock" based on the DEBUG mode checkbox.

## User Preferences

1. **Selection of Native and Target Language**: Users can select their native language and the target language for
   translation from a predefined list of languages. The selection retains a memory of the user's previous choices for
   convenience.
2. **Fluency Slider**: Users can adjust their level of fluency in the target language, from beginner (1) to expert (10),
   using a slider. This fluency level influences the complexity of the translated output and its explanation.
3. **Native Language Option**: A checkbox labeled 'View in native language' allows users to decide whether to have the
   story and comprehension questions displayed in their native language or the target language.

## Session State

1. **Persistence of Data**: The state of the session, including selected languages, fluency, game progress, and fetched
   articles, is maintained throughout the user's session.

## Translation

The **Translation** module offers users the capability to input text in their native language and receive its
translation in a chosen target language.
The module also provides an explanation of the translated text.

### Key Features

1. **Text Input Area**: Users can enter the text they wish to translate into the provided text area.
2. **Translation Execution**: By pressing the `Translate` button, the provided text will be translated into the selected
   target language. During the translation process, a spinner provides a visual cue to the user that processing is
   underway.
3. **Translation Output**: The translated text is presented in a new text area, and an explanation of the translation is
   displayed as an information box below.
4. **Debug Mode**: A 'Debug Mode' checkbox is included in the sidebar. This can be checked to debug the application
   using a mock model.

This feature leverages a powerful language model and is beneficial for language learners, international travelers, or
anyone needing quick, accurate translations with explanations.

## Storytime

The **Storyteller** module allows users to generate a unique story based on a provided concept and receive comprehension
questions related to the story.
The stories and questions can be presented in either the user's native language or a chosen target language.

### Key Features

1. **Concept Input**: Users provide a concept for their desired story. The concept can be a theme, a character, a
   setting, or any other idea around which the story will be constructed.
2. **Story Generation**: By pressing the 'Generate Story' button, users prompt the module to create a unique story based
   on the provided concept. A spinner displays during processing to indicate that the story is being generated.
3. **Story and Questions Output**: The generated story is displayed as markdown text, and comprehension questions
   related to the story appear below. Each question is accompanied by a checkbox that users can select to reveal the
   answer.

The Storyteller module, with its immersive and interactive approach to language learning, is an ideal tool for learners
seeking to improve their language skills through storytelling.
It harnesses the capabilities of a powerful language model to generate engaging content and comprehension questions
tailored to the user's fluency level.

## Playground

The **Playground** module provides users with an interactive platform to practice and enhance their language skills
through various activities. This module offers three main types of practice: translation, vocabulary, and grammar.

### Key Features

1. **Translation Practice**: In this activity, the user is presented with phrases in their target language. They can
   choose to reveal the translation of each phrase in their native language by checking the "Show Answer" box next to
   the phrase.
2. **Vocabulary Practice**: In this practice, the user encounters vocabulary words from their target language. They can
   reveal the translations of each word or phrase by checking the "Show Answer" box. The translations are displayed
   either as a list or a single string, depending on whether there are multiple translations available for a particular
   vocabulary item.
3. **Grammar Practice**: This activity presents users with sentences that contain a grammatical error (labeled "
   mistake"). The users can check the "Show Answer" box to view the corrected sentence, its translation, and an
   explanation of the error.

Each of these activities begins once the user clicks the "Start" button. A spinner indicates that the practice items are
being generated. After the generation is complete, the practice items (phrases, vocabulary words, or sentences) are
saved in the session state, so the user can revisit them during the same session.

## Chatterbox

The **Chatterbox** module is designed to create an interactive language learning environment for users, allowing them to
chat with a language model tutor in their chosen target language.

### Key features

1. **Conversation Input Method**: Users can choose to input their messages via text or voice. If the 'Voice Input'
   method is chosen, the user's spoken message is transcribed into text using the OpenAI Whisper ASR API.
2. **Bilingual Conversation History**: The history of the chat is kept track of in the user's chosen target language.
   This allows users to refer back to previous parts of the conversation.
3. **Language Tutor Feedback**: The AI language tutor offers feedback on the user's input, providing a corrected version
   and explanation if the user's message contained errors. These corrections are displayed in warning and information
   boxes for easy reference.
4. **Toggle Native Language View**: Users have the option to view the conversation in their native language. When
   toggled, this feature translates the conversation back into the user's native language.
5. **Message Exchange**: Messages are exchanged interactively between the user and the AI language tutor. The user's
   message inputs are marked distinctly for clarity in the chat history.

This feature uses advanced language models and is suitable for language learners of all levels, offering an engaging way
to practice a new language and receive instant feedback.

## Newsfeed

The **Newsfeed** module allows users to fetch, view, and translate news articles based on a specific keyword. It
enhances the learning experience by immersing users in real-world context in their target language.

### Key Features

1. **Customized News Retrieval**: Users can fetch news articles related to any keyword they're interested in. This not
   only provides a source of reading material that aligns with their interests but also aids in vocabulary acquisition
   within that particular field or context.
2. **News Translation**: Users can select any article from the fetched list to translate it into their target language.
   The translation includes the title, description, and content of the article.
3. **Interactive User Interface**: Each fetched article is displayed with a title, description, and content. If
   available, an image from the article is also displayed. For the full article, users are provided a 'Read more' link
   directing to the original source.

By integrating language learning with everyday context like news articles, the 'Newsfeed' module fosters a more engaging
and realistic learning experience. With its ability to cater to individual learning pace and content preferences, this
tool can prove invaluable for language learners at any level.

## Arcade

This **Arcade** module offers an engaging and interactive language learning experience with multiple game options
including Jeopardy, Pictionary, MadLibs, and Odd One Out. Each game provides a unique approach to practicing the target
language, enhancing vocabulary, fluency, and language comprehension in a fun, immersive environment.

### Key Features

1. **Variety of Games**: Users can choose to play one of four unique games, each designed to target different aspects of
   language learning:
    - Jeopardy: Users guess the answers to categorized questions in a classic Jeopardy format.
    - Pictionary: Users guess words or phrases based on images created in response to a prompt.
    - MadLibs: Users fill in the blanks of a story with appropriate words, receiving feedback upon submission.
    - Odd One Out: Users select the word that does not fit within a certain theme.
2. **Interactive Interface**: Streamlit's user-friendly interface provides dynamic game displays, immediate feedback,
   and maintains user scores.
3. **Real-time Feedback**: Upon submitting answers, users receive instant feedback and explanations, supporting their
   learning process.
4. **Score Tracking**: The module maintains a tally of the user's score, allowing them to track their progress and
   success throughout the games.

This 'Arcade' module provides a blend of fun and learning, allowing users to build language proficiency in an enjoyable,
game-based environment. It's a fantastic resource for language learners, leveraging gaming's motivation and competition
elements to enhance language acquisition.

## Culture Corner

The **Culture Corner** module is designed to provide interactive cultural information to the user. It uses Streamlit to
create an interactive web application with different services related to cultural information. Here are the key features
and functionalities:

### Key Features

1. **Selection of Services**: It offers three different services that the user can choose from - "Culture Info", "Plan a
   Trip", and "Cultural Faux Pas".
2. **Culture Info**: When this service is selected, the user can enter the name of a country and an optional region or
   city. On clicking the "Create Guide" button, a request is made to the "culture-info" service, and the resulting
   cultural information guide is displayed on the page.
3. **Plan a Trip**: This service allows the user to input various details related to a potential trip, including the
   destination country, start and end dates, budget, travel companions, and interests. The "Plan a Trip" button sends
   these details to the "culture-trip" service, which returns a trip plan that is displayed on the page.
4. **Cultural Faux Pas**: The user can input a country and an optional region or city, and then click the "Get Cultural
   Faux Pas" button to retrieve a list of cultural faux pas (blunders) for that location from the "culture-faux-pas"
   service.

All the services use the Vocava API to interact with the tutor and provide the requested information. This module
demonstrates a great way to create an interactive language and culture learning tool with Streamlit and a language
model.

# Vocava

## User Preferences
1. **Selection of Native and Target Language**: Users can select their native language and the target language for translation from a predefined list of languages. The selection retains a memory of the user's previous choices for convenience.
2. **Fluency Slider**: Users can adjust their level of fluency in the target language, from beginner (1) to expert (10), using a slider. This fluency level influences the complexity of the translated output and its explanation.
3. **Native Language Option**: A checkbox labeled 'View in native language' allows users to decide whether to have the story and comprehension questions displayed in their native language or the target language.

## Translation

The **Translation** module offers users the capability to input text in their native language and receive its translation in a chosen target language.
The module also provides an explanation of the translated text.

### Key Features

1. **Text Input Area**: Users can enter the text they wish to translate into the provided text area.
2. **Translation Execution**: By pressing the `Translate` button, the provided text will be translated into the selected target language. During the translation process, a spinner provides a visual cue to the user that processing is underway.
3. **Translation Output**: The translated text is presented in a new text area, and an explanation of the translation is displayed as an information box below.
4. **Debug Mode**: A 'Debug Mode' checkbox is included in the sidebar. This can be checked to debug the application using a mock model.

This feature leverages a powerful language model and is beneficial for language learners, international travelers, or anyone needing quick, accurate translations with explanations.

## Storytime

The **Storyteller** module allows users to generate a unique story based on a provided concept and receive comprehension questions related to the story.
The stories and questions can be presented in either the user's native language or a chosen target language.

### Key Features

1. **Concept Input**: Users provide a concept for their desired story. The concept can be a theme, a character, a setting, or any other idea around which the story will be constructed.
2. **Story Generation**: By pressing the 'Generate Story' button, users prompt the module to create a unique story based on the provided concept. A spinner displays during processing to indicate that the story is being generated.
3. **Story and Questions Output**: The generated story is displayed as markdown text, and comprehension questions related to the story appear below. Each question is accompanied by a checkbox that users can select to reveal the answer.

The Storyteller module, with its immersive and interactive approach to language learning, is an ideal tool for learners seeking to improve their language skills through storytelling.
It harnesses the capabilities of a powerful language model to generate engaging content and comprehension questions tailored to the user's fluency level.

## Playground
The **Playground** module provides users with an interactive platform to practice and enhance their language skills through various activities. This module offers three main types of practice: translation, vocabulary, and grammar.

### Key Features

1. **Translation Practice**: In this activity, the user is presented with phrases in their target language. They can choose to reveal the translation of each phrase in their native language by checking the "Show Answer" box next to the phrase.
2. **Vocabulary Practice**: In this practice, the user encounters vocabulary words from their target language. They can reveal the translations of each word or phrase by checking the "Show Answer" box. The translations are displayed either as a list or a single string, depending on whether there are multiple translations available for a particular vocabulary item.
3. **Grammar Practice**: This activity presents users with sentences that contain a grammatical error (labeled "mistake"). The users can check the "Show Answer" box to view the corrected sentence, its translation, and an explanation of the error.

Each of these activities begins once the user clicks the "Start" button. A spinner indicates that the practice items are being generated. After the generation is complete, the practice items (phrases, vocabulary words, or sentences) are saved in the session state, so the user can revisit them during the same session.

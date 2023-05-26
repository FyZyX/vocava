# Data Model

## User

- Represents a user on the platform.
- Fields: id, name
- Relationships: Messages they have sent, Translations they have submitted, Conversations they are part of through UserConversations

## Language

- Represents a language that can be spoken on the platform.
- Fields: id, name

## UserLanguage

- Represents a user's proficiency in a certain language.
- Fields: user_id, language_id, experience_points
- Relationships: User who speaks the language, Language being spoken

## Conversation

- Represents a conversation on the platform.
- Fields: id
- Relationships: Messages in the conversation, Users in the conversation through UserConversations

## UserConversation

- Represents a user's participation in a conversation, including the language they are using in that conversation.
- Fields: user_id, conversation_id, language_id
- Relationships: User in the conversation, Conversation being participated in, Language being used

## Message

- Represents a message sent in a conversation.
- Fields: id, user_id, conversation_id, content, language_id, timestamp
- Relationships: User who sent the message, Conversation the message was sent in, Translations of the message, Language of the message

## Translation

- Represents a translation of a message.
- Fields: id, message_id, user_id, content, timestamp
- Relationships: Message being translated, User who submitted the translation

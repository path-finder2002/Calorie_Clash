# Calorie Clash MVP GUI

---

## Features
- Minimal but beautiful GUI inspired by original game mechanics.
- Includes **Eat Phase Timer**: Players must finish the "eating" phase within 10 minutes, or be disqualified.
- 1P/2P modes.
- Target points setting.
- **Tie Rule Option**: Forbid reusing the tied hand in the next turn.
- Fullness gauge display.
- Animated transitions using Framer Motion.

## Immersive Eating Experience
- **Food Animation**: Animated bite effects or shrinking food images as time progresses.
- **Chewing Sound Effects**: Triggered on each click, tap, or key press to simulate eating.
- **Progressive Mess Effect**: Plate and table visuals change as food is consumed.
- **Haptic Feedback (Mobile)**: Subtle vibration feedback on each "bite" action.
- **Timer Pressure**: Timer pulses red and plays ticking sound near the deadline.

## Player Interaction Mechanics
- **Typing Challenge Mode** *(Custom Rule)*: During the eating phase, players must correctly type a series of random words or phrases within the time limit to simulate chewing and swallowing.
- **Button Mashing Mode**: Rapid key presses or clicks advance the eating progress.
- **Status-Based Consumption**: Eating speed and gauge progression depend on player stats (e.g., strength, stamina, hunger level).
- **Food-Specific Difficulty**: Different foods have unique bite resistance and calorie impact, affecting required inputs.

## Tech Stack
- React + Tailwind CSS + Framer Motion.
- Minimal dependencies for speed and portability.

## UI Components
- **Gauge**: Displays fullness progress and adjusts speed based on player stats.
- **HandButton**: Rock/Paper/Scissors selection.
- **PlayerCard**: Shows points, character selection, CPU difficulty.
- **RoundLog**: Displays round results and victory conditions.
- **FoodPlate**: Shows current food and bite progress.
- **TypingPrompt**: Displays random words/phrases the player must type to advance eating in Typing Challenge Mode.

## Eat Phase Timer
- When a player loses, they must “eat” the winner’s food within 10 minutes.
- Countdown timer displayed on screen.
- Failure to finish within the limit results in immediate disqualification.

## Setup Example
```bash
# Create project with Vite + React + TypeScript
yarn create vite calorie-clash-gui --template react-ts
cd calorie-clash-gui
yarn add framer-motion tailwindcss postcss autoprefixer
yarn tailwindcss init -p
# Configure Tailwind's content paths and import base styles
```

## Future Enhancements
- Dynamic food library with calorie data.
- Accessibility themes.
- Rule presets and save/load functionality.
- Online multiplayer mode with spectator chat and reactions.
